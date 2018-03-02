# Dissertation

The pervasiveness of smartphones has generated large amounts of data, whose analysis
can disclose valuable information regarding users' behaviour. At the same time, recent
advances in machine learning, especially on generalising the use of Convolutional Neural
Networks (CNN) on graphs, have allowed extending the use of deep learning beyond the
NLP and image recognition domains. In this project, we will explore the performance of
different machine learning techniques to the task of inferring demographics (age, gender,
job type) of the individuals from a graph representation of their mobile GPS location
data. The best performing model will be trained on the server and ported to a mobile
phone application which collects location data, builds mobility graphs from it and uses
the model and graphs to infer the demographics of the user locally on their device.
The main motivation of the project is to select a machine learning model and provide a
mobile framework for classifying users according to their mobility patterns, whilst keeping
their location data on their devices in order to prevent privacy leaks. A similar approach
has applicability to identifying stages of Alzheimer's Disease given a suitable data set,
since it has been observed that getting lost and misremembering the location of places
are symptoms that typify the onset of the disease, therefore their mobility graphs are likely to differ from the neurotypical which could be used for early diagnoses of the disease before
symptoms such as dementia and irreversible brain damage occur.
Two main issues need to be addressed to build such a system for this project. First, the
selection of a supervised classiffer to infer the user's demographic label. Recent advances
in Machine Learning have generalised CNNs from regular grid-like data such as images
and speech to irregular data like graphs as inputs. For this project, we will explore
the use of graph CNNs to infer individuals' demographic label from graph representations
of their mobile GPS location data collected with their mobile devices. We will study
how graph CNNs compares to traditional supervised learning approaches, from Logistic
Regression to Support Vector Machines, based on feature extraction of the graphs. We
will evaluate the performance by comparing the memory required, the speed of training
and making predictions with the models, and accuracy of the different approaches after
optimising each. For the input data into the models, we will create graphs with nodes for
locations and edges as transitions between locations in the period of observation.
Second, we need to provide a privacy-aware solution that guarantees the confidentiality
of the individuals sensitive location data and prevent privacy leaks by inferring the label
locally on the mobile device. To do so, we will build and train the model on a server by
using the dataset. This model will be then ported to a mobile phone application that
collects the location data, builds the graph and infers the demographic label locally. We
will also evaluate the performance of the model on the mobile application regarding its
time to build location graphs and infer the users class, as well as the battery consumption.

