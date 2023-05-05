# micro_expression_autism
This is the official implementation of our work about Face Micro-Expression Analysis on ADOS Videos for autism diagnosis.
This is an undergoing work.
Key codes and materials will be released after finsihed.


# introduction
Most previous study on facial expression analysis for ASD mainly focus on macro-expression analysis. However, micro-expression can reflect more true feelings of individuals. In our work, we use computer vision and machine learning technology to analyze facial micro-expressions of participants 
in hour-long ADOS video sequences for the diagnosis of ASD.


![arch](fig/diff.png)
![arch](fig/ME_samples.png)

Compared to Macro-expression, Micro-expressions are involuntary and transient facial expressions that can reflect the true emotions that a person try to suppress, hide, mask, or conceal, therefore, it provides more important information than macro-expression, especially in high-risk situations, like lie detection, criminal investigation, clinical diagnosis.


# pipeline

![arch](fig/ME_pipe.png)

It contains 4 parts: Pre-processing, Micro-expression Spotting, Feature extraction, and Classification.
First, face frames are extracted from the video by detection and cropping. 
Second, we use a spotting model to locate the Onset, apex, and Offset of each micro-expression movements.
Third, extract discriminative feature from each spotted segments.
Last, the final representation is fed for classification.

![arch](fig/ME_apex.png)

