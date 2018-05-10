# Face the Model
This project examines the efficacy of quickly building a model from scratch to classify images of one person’s face using readily available, open-source technologies.

## Background
From unlocking the iPhone X to tagging images on Facebook, facial recognition is becoming increasingly prevalent. Yet, Apple and Facebook have virtually unlimited resources for developing these technologies --  the rest of us have to make do with less. This begs a question: can an individual (or small organization) build an algorithm from scratch with open source technologies to detect images of one person's face with limited time and resources?

## The Challenge
To meet this challenge we'll first need to choose a model. How do we pick one model from an abundance of options? In 2012 the Super Vision algorithm won the ImageNet Large-Scale Visual Recognition Challenge by using a Convolutional Neural Network (CNN). This was a groundbreaking result that shifted the paradigm of computer vision. CNNs can be trained on relatively small datasets and without too laborious tuning. They also train relatively quickly on graphics processing units (GPUs). This will be our model of choice.

## The Data
We need to choose a person's face to detect -- our proxy. To keep things interesting, let's look for variation in the images. People change as they get older, so age will be our first variation. We'll need to gather lots of images of the proxy as a young adult, in middle age, and as a senior citizen. Since people tend to change their hair over the decades, hairstyles will be our second variation. We'll need images of our proxy with longer and shorter hair cuts. Finally, some people grow and shave facial hair throughout their lives -- a great option for our third variation. We'll need images of our our proxy with and without a mustache and beard.

Who should we choose? Paul McCartney has been an A-list celebrity since he was in his early 20s, and he's still an A-lister now that he is a septuagenarian. That means there are lots of images of him throughout his life (age). Further, he has had the famous Beatle's haircut, a mullet, and shorter hair over the years (hairstyle). Finally, he's been clean-shaven and has sported mustaches and beards at times (facial hair). He's a perfect choice for this proxy. Now we need get pictures of him.

We will source our images from two places. First, we will use the [Instagram Scraper](https://github.com/rarcega/instagram-scraper) to scrape Paul's page. Once we have pip installed instagram-scraper, we run the following command (replace the underscores with your sign-in credentials): instagram-scraper paulmccartney --login-user=___ --login_pass=__

Next, we will scrape Google Images for pictures of Paul. To help us download the images, we will leverage [Fatkun Batch Download Image](https://chrome.google.com/webstore/detail/fatkun-batch-download-ima/nnjjahlikiabnchcpehcpkdeckfgnohf?hl=en), a Google Chrome browser extension. Fatkun allows us easily select which images we want to download with a simple GUI. This is especially handy as we will not want to download every image that comes up per search. We filter our images that don't include Paul, images where most of Paul's face is obstructed, and images that are very low quality. We repeat this process for several searches (such as "Paul McCartney," "Paul McCartney mustache") until we have a few thousand images saved up. To keep things organized, we then move all the images to one folder. If we are working on a Mac, we can prevent issues with multiple images having the same name by leveraging the [Automator](https://www.wikihow.com/Batch-Rename-Files-in-Mac-OS-X-Using-Automator) to systematically rename files.

With all these images collected, it's possible that we have several duplicates throughout. Luckily, we can check for this by using the handy [Gemini 2](https://macpaw.com/gemini) application. Install the application and drag and drop the folder containing the images to scan for duplicates.

To train the CNN, we'll need lots of images of people other than Paul. Here we rely on the University of Illinois at Urbana-Champaign [FaceScrub](http://vintage.winklerbros.net/facescrub.html) dataset. This dataset has tens of thousands of images of actors and actresses. To get this data, you will need to fill out the [form](http://form.jotform.me/form/43268445913460) on the page to get access. You will then receive files with links to the images, as well as python code for downloading the images.

## Mechanics
For this challenge, we will need to leverage the power of GPUs. We will leverage GPU machines on Amazon Web Services (AWS). Setting up AWS can be it's own tutorial, so we'll skip the mechanics of how to do this here. We will need to upload our images to S3. First, we leverage the upload button in the S3 website. To ensure all our images have been properly uploaded, we use the [check_upload](https://github.com/srego/face_the_model/blob/master/Tools/S3/check_upload.py) script that I wrote for this challenge.

To use the GPU, we will need to set up a p2.xlarge machine on EC2. We then use the terminal to move files from S3 to EC2. Once the data is moved, we will leverage Kera's flow_from_directory infrastructure to easily segment the training and testing data. We will want to randomly segment our images into the training and testing datasets. The randomness helps ensure that we are not adding out own input into the image selection. To easily accomplish this, I created the [move_random_files script](https://github.com/srego/face_the_model/blob/master/Tools/EC2/move_random_files.py). For the best performing model (see below), we will use 1,585 training images per class (paul and not_paul) and 1,000 testing images per class.

## Model Architecture and Training
There are lots of ways to set up the CNN. We can choose different number of layers, different optimizers and learning rates, whether to use batch normalization, etc. There are literally thousands of implementation choices to make. I tried lots of models, and found that the most effective one is a four layer CNN connected to a four-layer Artificial Neural Network performed best. This model was inspired by [Super Data Science's
Deep Learning Udemy course](https://www.udemy.com/deeplearning/).

![Model](https://github.com/srego/face_the_model/blob/master/Model/model_image.png)

A few notes on the model:
* Convolutional Neural Network
  * All layers use 3 by 3 feature detector (kernel) sizes.
  * All layers apply padding to the input images.
  * The first two layers use 32 feature detectors, while the the layers use 64 feature detectors.
* Artificial Neural Network
  * The first and third layers use dropout.
  * The first three layers have 64 unit dimensions.
  * The last layer has a sigmoid activation function.

For more specifics, see the [model code](https://github.com/srego/face_the_model/blob/master/Model/best_model.py)

## Evaluation
To test how well the model did, we measure how many times the model correctly categorizes images it has not seen before. I tested the model against 842 Paul holdout images, 26,144 actor holdout images and 16,198 actress holdout images (from the FaceScrub dataset). The results, which can be seen in the [Jupyter Notebook](https://github.com/srego/face_the_model/blob/master/Model/best_model_test.ipynb), are promising. 95% of Paul images were correctly categorized while 67% of actor and 70% of actress images were correctly categorized. Great! With a little more effort, such as adding more training and testing images, we can probably improve the model. But, for now, this means that we have successfully met our challenge... right?

## Not so fast...
Not so fast! Watch what happens when we test the model against categories of images it has never seen before. Let's grab images of cats and dogs from the [Datasets & Templates](https://www.superdatascience.com/deep-learning/) section the Super Data Science Deep Learning A-Z page. What happens when we run the 1,000 and 842 cat and dog images through the model? Only 24% of these images were correctly categorized!

## Lesson
The most important lesson from this exercise is that a model is only as good as the data on which it is trained. Yes, we were able to quickly develop a model that  is pretty good at categorizing images of a single individual. But, this model is effective only when compared to images of other people. As soon as we introduced a category of data that the model was not trained on, it's accuracy declined dramatically. One way to solve this would be to create a model that identifies whether the image is that of a person and feed this model into the one we've built here.

Remember to always test your model! Throw in a curveball and see how it performs.
