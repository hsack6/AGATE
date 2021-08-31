# AGATE
This repository contains the code necessary to run the AGATE.  
See our report for details on the algorithm and the result.  
**Report link**: [Holistic Prediction on a Time-Evolving Attributed Graph](https://drive.google.com/file/d/1lHEKM9RcPX3vxBFQrTsOHGVwh_YZSCId/view?usp=sharing)

## Dataset
We created graph data from three datasets; [NBA](https://www.basketball-reference.com), [Reddit](http://snap.stanford.edu/data/soc-RedditHyperlinks.html), and [AMiner](https://www.aminer.cn/citation).  
Time-evolving attributed graphs for AGATE can be downloaded from [here](https://drive.google.com/drive/folders/1LM5_fOi__hHCpRAXJjTi445tTRYhRsNY?usp=sharing).  
Unzip graph.zip and place it under [DATASET]/data/ to run it.

## Code
You can find source code that works with each dataset in the AMiner, NBA, and Reddit.  
You can run AGATE by executing the scripts in the order described in run.sh  
All hyperparameters are described in setting_param.py.  
MakeSample has codes that create a dataset for a sub-prediction task.  
Model has codes for training methods of each subprediction task.  
Evaluation has codes for evaluating subprediction accuracy.
