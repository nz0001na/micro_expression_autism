# micro_expression_autism
This is the implementation of one of my work on Face Micro-Expression Analysis on ADOS Videos for autism diagnosis.
This work is an undergoing work. The key codes and materials will be released after work is done. stay tuned!

# introduction
Facial expression analysis has attracted great interest over the past years. It can be used in many real-life applications, like digital health, human machine interaction, behavior analysis, video communication, etc.

People with autism spectrum disorder (ASD) show socio-emotion interaction difficulties in communication disorder, emotional dysregulation with rigid and repetitive behaviors. These difficulties cause many problems related to performance of expressive language, social and emotional adaptive skills. People with autism usually do not show their emotions in a way that normal people would be able to recognize and understand. Either they do not respond emotionally, or their emotional responses might sometimes seem over-reaction.

Most previous study on facial emotion analysis for ASD mainly focus on macro-expression analysis, which is easily noticed and voluntary with long duration, large muscle variation. However, micro-expression, which is easy to ignore, involuntary, uncontrollable, and spontaneous with short duration and slight variation, often reflects the true feelings that a person try to conceal, hide, mask or suppress, especially important in high-risk situations, like clinical diagnosis, lie detection, and criminal investigation. 
![arch](fig/diff.png)

In our work, we use computer vision and machine learning technology to analyze facial micro-expressions of participants in hour-long ADOS video sequences for the diagnosis of ASD.
![arch](fig/ME_samples.png)


# pipeline

![arch](fig/ME_pipe.png)

It contains 4 steps: Pre-processing, Micro-expression Spotting, Feature extraction, and Classification.

(1) First, face frames are extracted from the video by detection and cropping.  

![arch](fig/step1.png)

(2) Second, locate the Onset, apex, and Offset of each micro-expression movements in the videos. 
![arch](fig/ME_apex.png)

onset: the first frame at which a Micro-Expression (ME) starts. i.e., changing from the baseline, which is usually the neutral facial expression.

apex: the frame at which the highest intensity of the facial expression is reached.

offset: the last frame at which a ME ends, i.e., returning back to the neutral facial expression.

![arch](fig/step2.png)

(3) Third, extract discriminative facial subtle muscle movement change feature from each spotted micro-expression subvideo. 

we use a BERT-based Auto Encoder as a base model (https://github.com/uark-cviu/Micron-BERT) to capture these micro-changes of facial texture in an unsupervised manner.

It consists of five main blocks. 

Two input frames(onset and apex) are first divided into a set of several non-overlapping patches, respectively.

(a) patch-wise Swapping: randomly swap patches between onset and apex frames to create a swapped image.

(b) Encoder: represent input into latent vectors. 

(c) Patch of Interest (PoI): enable the model to look into facial regions containing micro-expressions, not unrelated regions, like background.

(d) Diagonal Micro Attention (DMA): allow the model to focus on facial regions that primarily consist of micro differences between frames.

(e) Decoder: reconstructs the output signal using latent code.

![arch](fig/step3.png)

The final feature (F_DMA) captures the micro-changes between apex and onset, and micro-changes in facial regions.
It can be a discriminative feature of micro-expression.

(4) Last, the final representation is fed into SVM for final classification.

### Link: 
More details can be referred to my thesis(Section 4.4). 
[[PDF]](https://researchrepository.wvu.edu/etd/11861/)


