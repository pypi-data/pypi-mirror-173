# Overview

The notebooks include educational examples, dataset cleaning, models that are benchmarked and
a set of replications. At the end of this document resources are listed that I found to be
useful.


# Examples

The example notebooks serve an educational purpose to show how models can be build in 
conjunction with  *pyadlml*. The notebooks
review a bit of theory backing the models, followed by a simple proof of concept and 
an application to one dataset.

- [RNN]()
- [HMM]()
- [HSMM]()

# Datasets

Most datasets are in a desolate state. To properly evaluate models cleaned up dataset versions 
are used. By passing the parameter `load_cleaned=True` to the `fetch_dataset` method a preprocessed 
dataset is loaded. The reasoning for the measures and cleaning steps taken are tracked for all datasets:

- [Aras]()
- [Mitlab]()
- [Tuebingen 2019]()
- [Casas Aruba]() 
- [MITLab]() 
- [Casas Milan]() 

# Models

This is a thoroughly gathered performance comparison between many models. Emphasize is on
the performance and not learning. For each category a survey is done to get retrieve the
best performing models. The total survey provides a ranking of the overall best performing
models.

- I.I.d.
    - [Random Forest]()
    - [SVM]()
    - [Naive Bayes]()
    - [Survey]()    
- Sequential
    - Discrete
        - ordered
        - timeslice
            - [Recurrent Neural Network]()
            - [InecptionTime]()
            - [Rocket]()
            - [Bernoulli Hidden Markov Model]()
            - [Bernoulli Semi-Hidden Markov Model]()
            - [Continuous Hidden Markov Model]()
        - [Survey]()
    - Continuous
        - ordered 
        - temporal points
            - marked temporal hawkes process
            - marked temporal poisson process
        - [Survey]()
    - [Total Survey]()
# Replications

The following sections provides links to 

- [Neural Network Ensembles for Sensor-Based Human Activity Recognition Within Smart Environments](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6982871/)
  - a 
  - notebook link
- [Human Activity Recognition using Recurrent Neural Networks](https://arxiv.org/abs/1804.07144v1)
  - LSTMS on
  - notebook link
- [A sequence-to-sequence model-based deep learning approach for recognizing activity of daily living for senior care](https://www.sciencedirect.com/science/article/pii/S1532046418301321)
  - LSTMS on 
  - notebook link
- [Online Human Activity Recognition Employing Hierarchical Hidden Markov Models](https://arxiv.org/abs/1903.04820v1)
  - Hierachical HMM on 
  - notebook link
- [Activity Recognition using Hierarchical Hidden Markov Models on Streaming Sensor Data](https://arxiv.org/abs/1810.05504)
  - asd  
  - notebook link
- [An Evaluation on ModelsforParticle Filtering forResidentTracking in a Smart Home using Binary Sensors](https://www.semanticscholar.org/paper/An-evaluation-on-models-for-particle-filtering-for-Ngamakeur-Yongchareon/7eed553289acfc63e6543036a7e0bbdea374358f)
  - Particle Filter on ARAS
  - notebook link
- [Human Activity Recognition from Wireless Sensor Network Data: Benchmark and Software](https://www.researchgate.net/publication/227017257_Human_Activity_Recognition_from_Wireless_Sensor_Network_Data_Benchmark_and_Software?enrichId=rgreq-79cd6d6f95a28ab0402049a013091deb-XXX&enrichSource=Y292ZXJQYWdlOzIyNzAxNzI1NztBUzoxMDM0MzU2MTc3MDE4OTFAMTQwMTY3MjM4MTc1OA%3D%3D&el=1_x_3&_esc=publicationCoverPdf)
  - Kasteren dataset, apply Naive Bayes HMM, CRF on Kasteren House A,B,C 
  - notebook link
- [Activity Recognition using semi-MarkovModels on Real World Smart Home Data Sets](https://www.researchgate.net/publication/220497536_Activity_recognition_using_semi-Markov_models_on_real_world_smart_home_datasets)
  - Semi HMMs and CRF on Ubicomp, Placelab
  - notebook link
- [Using Bayesian Networks for Daily Activity Prediction](https://www.researchgate.net/publication/282051479_Using_bayesian_networks_for_daily_activity_prediction) 
  - CRAFFT, really cool bayesian network approach to modelling data
  - notebook link  

## Resources

The following links are papers, blogs or resources that I found to be useful and relevant to 
the subject at hand. Firstmost a few review articles


#### Surveys
- [Activity and Anomaly Detection in Smart Home](https://link.springer.com/chapter/10.1007/978-3-319-21671-3_9), 
  - A survey paper ADLs
- [Evaluation of Three State-of-the-Art Classifiers for Recognition of Activities of Daily Living from Smart Home Ambient Data](https://pubmed.ncbi.nlm.nih.gov/26007727/)
  - todo 
- [Evaluating Machine Learning Techniques for Activity Classification in Smart Home Environments](https://www.researchgate.net/publication/322978518_Evaluating_Machine_Learning_Techniques_for_Activity_Classification_in_Smart_Home_Environments?enrichId=rgreq-60f496a6b2df9a0590a5ba8d66dfeff1-XXX&enrichSource=Y292ZXJQYWdlOzMyMjk3ODUxODtBUzo1OTE0NzEwNTcwNjgwMzJAMTUxODAyOTA5NzMwNw%3D%3D&el=1_x_3&_esc=publicationCoverPdf)
  - A survey including SVMs, HMM, HTM, LSTM, CNNs, on ARAS, 
- [A Review of Smart Homes – Past, Present, and Future](https://www.researchgate.net/publication/262687986_A_Review_of_Smart_Homes_-_Past_Present_and_Future)
  - todo 
  
    
#### Other Models
- [Activity Recognition in New Smart Home Environments](https://dl.acm.org/doi/10.1145/3264996.3265001)
  - Transfer from one home into another. ARAS
- [On Multi-resident Activity Recognition in Ambient Smart-Homes](https://arxiv.org/abs/1806.06611), 
   - multi resident prediction using RNNs, HMMs, and CRNs
- [Deep Neural Networks for Activity Recognition with Multi-Sensor Data in a Smart Home](https://www.researchgate.net/publication/325025722_Deep_neural_networks_for_activity_recognition_with_multi-sensor_data_in_a_smart_home)
- [Human Activity Prediction in Smart Home Environments with LSTM Neural Networks](https://www.researchgate.net/publication/326344950_Human_Activity_Prediction_in_Smart_Home_Environments_with_LSTM_Neural_Networks?enrichId=rgreq-3ba71fb9e0d9d7ff54122f94b16f644f-XXX&enrichSource=Y292ZXJQYWdlOzMyNjM0NDk1MDtBUzo2NDc0NjUzODQ1NTA0MDBAMTUzMTM3OTE4NTg4Ng%3D%3D&el=1_x_3&_esc=publicationCoverPdf)
  - Predicts next device activities with LSTMS on CASAS and ARAS.

#### Misc
- [Human-Activity-Recognition](https://github.com/du-phan/Human-Activity-Recognition)
  - A github repo providing examples
- [Casas Dataset](http://ailab.wsu.edu/casas/datasets.html)
  - A lot more datasets on activity recognition. Some are 
  not labeled. 
- [Activity Recognition using Hierarchical Hidden Markov Models on Streaming Sensor Data](https://www.researchgate.net/publication/328280620_Activity_Recognition_using_Hierarchical_Hidden_Markov_Models_on_Streaming_Sensor_Data)
  - Hierarchical models
  - On dataset that is no more availabl
- [A Markovian-based Approach for Daily Living Activities Recognition](https://www.researchgate.net/publication/301721523_A_Markovian-based_Approach_for_Daily_Living_Activities_Recognition)
  - Try to create a hierachy of room to activity to sensor mapping
  - No dataset is used 
