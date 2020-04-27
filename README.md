# Does-Hulk-Live-Here
A Reddit bot written in Python, using praw and boto3 to make API calls to Reddit to parse post streams, and downloads any image (.png or .jpg) that it finds, uploads this to S3 storage, which has a Rekognition custom label that I trained run against it to determine if The Hulk is present in that image. Only then will it upvote. The bot is running on a free AWS t2.micro EC2.
