from torch.autograd import Variable
import os
from scipy.sparse import lil_matrix
from scipy.io import mmwrite
os.environ['KMP_DUPLICATE_LIB_OK']='True' # mmwriteー


def inference(dataloader, opt, OutputDir, Attribute_idx):
    for i, (sample_idx, annotation, adj_matrix, label, mask) in enumerate(dataloader, 0):
        target = Variable(label)
        mask = Variable(mask)
        output = annotation[:, :, -1][:, :, Attribute_idx]

        #
        os.makedirs(OutputDir + "/output", exist_ok=True)
        for batch in range(opt.batchSize):
            p = output.detach().numpy()[batch]
            t = target[batch].numpy()
            m = mask[batch].numpy()
            mmwrite(OutputDir + "/output/pred" + str(sample_idx.numpy()[batch]), lil_matrix(p))
            mmwrite(OutputDir + "/output/true" + str(sample_idx.numpy()[batch]), lil_matrix(t))
            mmwrite(OutputDir + "/output/mask" + str(sample_idx.numpy()[batch]), lil_matrix(m))
