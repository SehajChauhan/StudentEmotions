<p align="center">
  <img width="15%" src="https://i.ibb.co/478DZ4f/greylogo.png">
</p>
# StudentEmotions<br>
### Introduction 
The COVID-19 pandemic and the resulting economic recession have negatively affected the mental well being of all kinds of individuals, a particular section of these being university students. Institutions of higher education worldwide are undergoing unprecedented change because of the COVID-19 pandemic. Universities and colleges have been forced to switch to online teaching and learning. In this project, I analyze the perceived difference of post and comment sentiments from various university communities on Reddit between the years; 2019 and 2020 as more and more of these educational changes were put into application. 
 
### Tools and Services Used 
- **Pushshift API:** An open source API created by the /r/datasets mod team to help provide enhanced functionality and search capabilities for searching Reddit comments and submissions. For analysis purposes, Pushshift provides more flexibility and better call quotas than Reddit’s official API.<br>
- **Python:** The primary language in which the project is created. In addition to default libraries, Boto3 (AWS SDK for Python) was used to access and write the content to an S3 bucket, Pandas and Numpy for data manipulation and analysis. Tensorflow and Keras for ML modelling and evaluation.<br>
- **AWS Lambda:** The primary compute infrastructure of the project. Multiple serverless Lambda functions execute the code in a parallel process and pull content from different subreddits at the same time.<br>
- **AWS Step Functions:** Used to run a JSON script that invokes the lambda functions and supplies the parameters. 
- **S3:** The primary storage service for the project.<br>
- **AWS Sagemaker notebook instances:** Managed high performance virtual instance running a Jupyter notebook for data analysis. 


### Data
A data compilation of sentiment labelled tweets from various resources was used to train and evaluate the model. 


### Model
Using Keras, I created a Recurrent Neural Network (RNN) model that works with sequential data. The RNN algorithm trains a neural network in loops with the network gaining information from the previous steps. 
During the training process, the information repeatedly loops resulting in larger information updates to the network weights which causes an accumulation of error gradients during each update making the network unstable. If the update sizes reach an extreme, they might start to overflow and result in NaN values. To overcome this problem a technique called Long Short-Term Memory (LSTM) is used. LSTM can capture long-range dependencies. It can keep memory about previous inputs for extended time durations.
The first layer of the model is the Embedding layer. It represents the unique words of the dataset in vector form and primarily used to compress the input feature space into a smaller one. This compression then makes the computation of sentences faster. The input dimension for this layer is 5000 of the most commonly used words in the dataset and the output dimension is 64 ie. the size of the output vectors from this layer for each word. 
A SpatialDropout Layer is used to prevent the model from Overfitting.
The second is a LSTM layer followed by a dropout layer. Its 64 cells (each cell has its own inputs, outputs and memory) are used and the return sequence is set to true which means that every time there will be an output which will be fed into another LSTM layer it is sent as a sequence rather than a single value of each input.
The final layer will be a Dense layer with 2 units for the two classes present and the activation is set to softmax which returns a probability distribution over the target classes.
The optimizer used is ‘adam’ as it is really efficient for working with large datasets.

<p align="center">
  <img width="45%" src="https://i.ibb.co/0D57359/model-plot.png">
</p>

The model is then set to train for 3 epochs. The training process took about 13 minutes/epoch to be completed with the high compute performance of the sagemaker notebook instance.
In evaluation the model achieved,<br>
- **Accuracy: 0.9861490482847618**
- **F1 Score: 0.9869397463286533**
- **AUC ROC: 0.9861601844657049**
- **Log Loss: 0.42481298574916665**


### Insights
Below are the insights that extracted from the data scraped off reddit. <br>
- There was an overall increase of **0.741%** in emotionally depressed posts across reddit communities of all universities in Ontario.
- There was an overall increase of **0.977%** in emotionally depressed comments on the posts across reddi communities of all universities in Ontario 
- In 2019 the least emotionally depressed posts were posted in Brock University as **37.382%** of the total posts.
- In 2019 the most emotionally depressed posts were posted in **University of Toronto Mississauga** as **42.516%** of the total posts.
- In 2019 the most emotionally depressed interactions took place in **The University of Waterloo** as **42.253%** of the total comments.
- In 2019 the least emotionally depressed interactions took place in **The University of Gueplh** as **36.336%**  of the total comments.
- In 2020 the least emotionally depressed posts were posted in **Brock University** as **35.273%**  of the total posts.
- In 2020 the most emotionally depressed posts were posted in **McMaster University** as **43.516%** of the total posts.
- In 2020 the most emotionally depressed interactions took place in **The University of Waterloo** as **43.667%** of the total comments.
- In 2020 the least emotionally depressed interactions took place in **Trent University** as **34.81%** of the total comments.
- Between the years 2020 and 2019, **University of Waterloo**'s subreddit was observed to get the highest gain in new subscribers with a **43.31% increase**.


### Drawbacks
The results of the analysis were not as great as I was expecting. Primarily this was due to how my ML model made predictions. Since the model was trained on short sentences ie. tweets, it didnt really perform up to the mark with reddit posts with long blobs of content. Try as hard as I could, I was unable to find data to train the model for a more accurate sentiment analysis of longer pieces of text.


### Future 
I will continue my search for the required dataset, or a different way to analyze long pieces of text. The scraper is also a great tool for easily extracting large chunks of content from reddit for analysis and I might work with it for different projects.  

