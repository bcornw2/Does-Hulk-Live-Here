import praw
import boto3
import os

USER_AGENT = "ec2-aws_rekognition-bot:v1.0.0"

if not os.path.isfile("/home/ec2-user/doesHulkLiveHere/posts_replied_to.txt"):
    posts_replied_to =[]
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

reddit = praw.Reddit(client_id='MyKX7rKZ4NxquA',
        client_secret='x-IWsKKJLB6voexds0w8FnvHv38',
        username='DoesHulkLiveHere_bot',
        user_agent='USER_AGENT')

client = boto3.client('rekognition',
        aws_access_key_id = 'AKIAIRGQAQXDAQ3NPA2Q',
        aws_secret_access_key = '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',
        region_name='us-east-1')

subreddit = reddit.subreddit('doeshulklivehere')


def upload_image(url):
    file = open('/home/ec2-user/doesHulkLiveHere/imageCount.txt', 'r')
    first_line = file.readline()
    for last_line in file: 
        pass
    num = int(last_line)+1
    file.close()
    count = str(num)

    image_name = 'hulk' + count + '.jpg'
    
    ImgurDownloader(url, '/home/ec2-user/doesHulkLiveHere/scratch/',image_name)
    image_path = os.path.join('/home/ec2-user/doesHulkLiveHere/scratch/', image_name)

    s3_client = boto3.client(s's3')
    try:
        response = s3_client.upload_file(image_path, 'hulkimages', imagepath)
    except ClientError as e:
        logging.error(e)
        return False
    os.remove(image_path)
    return True
    


def detect_labels(photo, bucket):
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}}, MaxLabels=10)

    print('detected labels for: ' + photo)
    print()
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']))
        print ("Instances:")
        for instance in label['Instances']:
            print ("  Bounding box")
            print ("    Top: " + str(instance['BoundingBox']['Top']))
            print ("    Left: " + str(instance['BoundingBox']['Left']))
            print ("    Width: " +  str(instance['BoundingBox']['Width']))
            print ("    Height: " +  str(instance['BoundingBox']['Height']))
            print ("  Confidence: " + str(instance['Confidence']))
            print()

        print('Parents:')
        for parent in label['Parents']:
            print ("   " + parent['Name'])
        print("-------------")
        print()
    return len(response['Labels'])

def process_submission(submission):
    now = datetime.datetime.now()
    try:
        with open("posts_replied_to.txt", "a") as file:
            file.write(submission.id + "\n")
            with open("logfile.txt", "a") as log:
                log.write(now.strftime("%Y-%m-%d %H:%M") + "Submission ID: " + submission.id + "Comment Body: " + submission.selftext + "\n Reply: " + message + "\n ================================== \n")
            submission.reply(message)
            print("SUBMISSION IS: " + str(submission.title))
            print(" :: SUBMISSION REPLY SENT :: ")
        except APIException as e:
                    print("error!: {0}".format(e))


def main():
    photo='hulk1.jpg'
    bucket='hulkimages'
    label_count=detect_labels(photo, bucket)
    print("Labels detected: " + str(label_count))

    
    while True:
        for submission in subreddit.stream.submissions(pause_after=0,skip_existing=True):
            print("  =  =  find submission")
            try:
                if submission is None:
                        print("Submission of type None")
                        break
                if submission.id not in posts_replied_to:
                    print("bot replying to submission id:  " +  submission.id)
                    with open("posts_replied_to.txt", "a") as file:
                        file.write(submission.id + "\n")
                    process_submission(submission)
                else:
                    break
            except AttributeError as e:
                    print("Error! under submission : {0}".format(e))




if __name__ == "__main__":
    main()
