# Face the Model
This project examines examines the efficacy of quickly building a model from scratch to classify images of one person’s face using readily available, open-source technologies.

## Background
From unlocking the iPhone X to tagging images on FaceBook, facial recognition is becoming increasingly prevalent. Yet, Apple and FaceBook have virtually unlimited resources for developing these technologies --  the rest of us have to make do with less. This begs a question: can an individual (or small organization) build an algorithm from scratch with open source technologies to detect images of one person's face with limited time and resources?

## The Challenge
To meet this challenge we'll first need to choose a model. How do we pick one model from an abundance of options? In 2012 the Super Vision algorithm won the ImageNet Large-Scale Visual Recognition Challenge by using a Convolutional Neural Network (CNN). This was a groundbreaking result that shifted the paradigm of computer vision challenges. CNNs can be trained on relatively small datasets and without too laborious tuning. They also train relatively quickly on graphics processing units (GPUs). This will be our model of choice.

## The Data
We need to choose a person's face to detect -- our proxy. To keep things interesting, let's look for lots variation in the images. People change as they get older, so age will be our first variation. We'll need to gather lots of images of the proxy as a young adult, in middle age, and as a senior citizen. Since people tend to change their hair over the decades, hairstyles will be our second variation. We'll need images of our proxy with longer and shorter hair cuts. Finally, some people grow and shave facial hair throughout their lives -- a great option for our third variation. We'll need images of our our proxy with and without a mustache and beard.

Who should we choose? Paul McCartney has been an A-list celebrity since he was in his early 20s, and he's still an A-lister now that he is a septuagenarian. That means there are lots of images of him throughout his life (age). Further, he has had the famous Beatle's haircut, a mullet, and shorter hair over the years (hairstyle). Finally, he's been clean-shaven and has sported mustaches and beards at times (facial hair). He's a perfect choice for this proxy. Now we need get pictures of him.

We will source our images from two places. First, we will use the [Instagram Scraper](https://github.com/rarcega/instagram-scraper) to scrape Paul's page. Once we have pip installed instagram-scraper, we run the following command (replace the underscores with your sign-in credentials): instagram-scraper paulmccartney --login-user=___ --login_pass=__

To train the CNN, we'll need lots of images of people other than Paul. Here we rely on the University of Illinois at Urbana-Champaign [FaceScrub](http://vintage.winklerbros.net/facescrub.html) dataset. This dataset has tens of thousands of images of actors and actresses. To get this data, you will need to fill out the [form](http://form.jotform.me/form/43268445913460) on the page to get access. Please feel free to message me if you have issues with this step.

## Training
 
