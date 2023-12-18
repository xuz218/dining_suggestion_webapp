# dining_suggestion_webapp

## AWS Architecture
![aws-architecture](https://github.com/xuz218/dining_suggestion_webapp/assets/88963429/10dc040b-1353-4964-b87f-02c5b28d3975)

## Directory structure
1. [static](./static):
   Static files of flask project, sdk generated from api gateway. 

2. [templates](./templates):
   Front-end files of flask project, including all html files, the [index.html](./templates/index.html) is our main page. 

3. [app.py](./app.py):
   Flask project manager for running the flask server.

4. [lambda functions](./lambda function):
   Lambda functions deployed on AWS, detailed descriptions could be found in the paper.  

## EC2 directions
**Reference websites**: https://www.twilio.com/blog/deploy-flask-python-app-aws
### Instruction for running：
1. ssh into ubuntu
2. cd to deployedapp path
3. running command：```flask run --host=0.0.0.0 --port=8080```
4. broswer link：```44.204.18.251:8080```

### Config Procedure (can be ignored after configured once)：
### SSH into EC2 ubuntu terminal from local machine
- Go to the directory storing your ssh key "diningdbec2keypair.pem" （put key in the same directory as project code）
  - **change permission**:
    restrict read and write permissions to the private key file.
    ```bash
    local machine $ chmod 600 ./diningdbec2keypair.pem
    ```
  - **Set up ssh environment**:
    This command adds SSH private keys into the SSH authentication agent in order to have single sign-on options.
    ```bash
    local machine $ ssh-add ./diningdbec2keypair.pem
    ```
  - **SSH to EC2 terminal on AWS**:
    ```bash
    local machine $ ssh -i diningdbec2keypair.pem ubuntu@ec2-44-204-18-251.compute-1.amazonaws.com
    ```
    Expected success response: ```ubuntu@ip-172-31-84-223:~$```

### Ubuntu Shell Enviornment Config
- Install tmux (session management):
  ```
  ubuntu@ip-172-31-84-223:~$ sudo apt update
  ubuntu@ip-172-31-84-223:~$ sudo apt install python3 python3-pip tmux htop
  ```

### Transfer your project files to remote host
- make a new empty folder, ready for our deployment:
  ```
  ubuntu@ip-172-31-84-223:~$ mkdir deployedapp
  ```
- If you just want to test the EC2, just pull code from **temp_ec2** branch to your local machine, which has everything prepared and ready to launch, then you can skip next step
- Otherwise, Go to dining_suggestion_webapp directoy and run:
  ```
  localmachine $ pip freeze > requirements.txt
  ```
- Transfer the project:
  ```
  localmachine $ sudo rsync -rv /Users/yizhenzhang/Desktop/dining_suggestion_webapp/ ubuntu@44.204.18.251:/home/ubuntu/deployedapp
  ```
  - ```/Users/yizhenzhang/Desktop/dining_suggestion_webapp/``` is the location on local machine
  - ```/home/ubuntu/deployedapp``` is the new empty folder on ubuntu
  - ```44.204.18.251``` the public ipv4 ec2 address
- Now you can see the entire project code in deployedapp folder on ubuntu ssh terminal

### Deploy the application on EC2 instance
- Run: 
  ```
  ubuntu@ip-172-31-84-223:~$ tmux new -s mytestapp
  ```
  - which redirect us to the “mytestapp” tmux session
 
- Install all requirements:
  ```
  ubuntu@ip-172-31-84-223:~$ pip install -r requirements.txt
  ```
  or pip install manually yourself (更靠谱)
- Start the server in ubuntu:

  ```
  ubuntu@ip-172-31-84-223:~/deployedapp$ flask run --host=0.0.0.0 --port=8080
   * Environment: production
     WARNING: This is a development server. Do not use it in a production deployment.
     Use a production WSGI server instead.
   * Debug mode: off
   * Running on all addresses.
     WARNING: This is a development server. Do not use it in a production deployment.
   * Running on http://172.31.84.223:8080/ (Press CTRL+C to quit)
  ```
  - NOTE: **http://172.31.84.223:8080/ is only the private ec2 address, inorder to access the webpage from browser:**
  1. **go to aws console ec2**:
      ```EC2 > Security Groups > sg-03256dee1dca25fab - default```
  2. **Add a role** (I allow every access, maybe you have safer way...):
    <img width="1174" alt="Screenshot 2023-12-18 at 12 13 14 AM" src="https://github.com/xuz218/dining_suggestion_webapp/assets/98562104/d5711c49-a562-4f45-a1d6-aacf3d3fb425">
    
  3. **Access the browser with the public ip address of ec2**: 44.204.18.251:8080


  

