from torch.autograd import Variable
import torch
import numpy as np
import random
import networkx as nx

import sys
import os
current_dir = os.path.dirname(os.path.abspath("__file__"))
sys.path.append( str(current_dir) + '/../../../' )
from setting_param import all_node_num
from setting_param import n_expanded

def _random_subset(seq,m):
    targets=set()
    while len(targets)<m:
        x=random.choice(seq)
        targets.add(x)
    return targets

def balancer(target, mask):
    target = target[0 < mask]
    n_positive = int(target.sum())
    n_negative = int(len(target) - n_positive)
    if n_positive <= n_negative:
        sample_idx_list = np.where(target==1)[0].tolist()
        negative_idx = np.where(target==0)[0]
        sample_idx_list.extend(list(_random_subset(negative_idx, n_positive)))
    else:
        sample_idx_list = np.where(target==0)[0].tolist()
        positive_idx = np.where(target==1)[0]
        sample_idx_list.extend(list(_random_subset(positive_idx, n_negative)))
    return sample_idx_list

def train(epoch, dataloader, net, criterion, optimizer, opt):
    train_loss = 0
    net.train()
    for i, (sample_idx, annotation, label_, mask_, indic) in enumerate(dataloader, 0):
        net.zero_grad()
        padding = torch.zeros(opt.batchSize, opt.n_node, opt.state_dim - opt.annotation_dim).double()
        init_input = torch.cat((annotation, padding), 2)

        label = []
        mask = []
        for batch in range(label_.shape[0]):
            label_graph = nx.Graph()
            label_graph.add_edges_from(label_[batch].numpy())
            label.append(nx.to_numpy_matrix(label_graph, nodelist=list(range(all_node_num + n_expanded))))

            mask_graph = nx.Graph()
            mask_graph.add_edges_from(mask_[batch].numpy())
            mask.append(nx.to_numpy_matrix(mask_graph, nodelist=list(range(all_node_num + n_expanded))))
        label = torch.tensor(np.array(label), dtype=torch.double)
        mask = torch.tensor(np.array(mask), dtype=torch.double)

        if opt.cuda:
            init_input      = init_input.cuda()
            label = label.cuda()
            mask = mask.cuda()

        init_input      = Variable(init_input)
        target = Variable(label)
        mask = Variable(mask)

        output = net(init_input, indic, mask_)
        sample_idx_list = balancer(target.numpy(), mask.numpy())
        if len(sample_idx_list) == 0: # posneg
            loss = criterion(output[0<mask], target[0<mask])
        else:
            loss = criterion(output[0 < mask][sample_idx_list], target[0 < mask][sample_idx_list])

        #loss.backward()
        #optimizer.step()

        train_loss += loss.item()

        if i % int(len(dataloader) / 10 + 1) == 0 and opt.verbal:
            print('[%d/%d][%d/%d] Loss: %.4f' % (epoch, opt.niter, i, len(dataloader), loss.item()))

    train_loss /= (len(dataloader.dataset) / opt.batchSize)
    print('Train set: Average loss: {:.4f}'.format(train_loss))

    return train_loss
