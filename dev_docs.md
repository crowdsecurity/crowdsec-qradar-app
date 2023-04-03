This document goes through setting up the development environment for CrowdSec QRadar App. It also goes through common development workflows.


## Setting up QRadar Instance

### Installation

You'll need to follow the below-mentioned guide. Some things to note:

- Use instance from m5 series (We've used m5.2xlarge). The recommended series `m4` didn't work for us and failed to even boot up.

- Make sure you set up the VPC as mentioned in the guide. The installation will fail if default VPC is used.

- Make sure you've 250 GB of secondary storage. The installation will fail if you don't have enough space or don't have secondary storage.


Follow this [guide](https://www.ibm.com/docs/en/qsip/7.4?topic=qcmi-configuring-qradar-743-virtual-appliance-amazon-web-services).



During the last step of the guide, use the following command to start the installation:

```bash
sudo /root/setup 3199
```

The installation takes around 45-60 minutes on m5.2xlarge

### Configuration

#### Setting the admin password

Use the following command

```bash
sudo /opt/qradar/support/changePasswd.sh -a
```

It'll ask for and confirm the new password.

Then restart the server via:

```bash
sudo systemctl restart tomcat
```

You should be able to login to the QRadar console now by going to `https://<instance-ip>`

#### Creating Authorized service

Certain tasks in QRadar require an authorized service. You can create one by following this [guide](https://www.ibm.com/docs/en/qradar-common?topic=app-creating-authorized-service-token-qradar-operations)

#### Installing Apps for development and validation

We need to install certain Apps which make it easy for deploying QRadar Apps. See this [guide](https://www.ibm.com/docs/en/qsip/7.4?topic=content-installing-extensions-by-using-extensions-management) which shows how to install Apps.

The specific Apps to be installed are:

- [QRadar Pre-Validation App](https://exchange.xforce.ibmcloud.com/hub/extension/2a981b2408592beff74ff0f936cd46db): This is used to validate the App before publishing it. It also outputs a report which is necessary to provide to X-Force Exchange team for publishing the App.

- [QRadar App Editor](https://exchange.xforce.ibmcloud.com/hub/extension/5d0f3f37cc5c4d16ccafe9d40d8dffe5): This enables relatively quick deployment of Apps.

## Setting up the development environment

### Pre-requisites

- Python 3.6.10 is recommended.
- Jarsigner. It's bundled with JDK.
- make
- docker


### Installing QRadar App SDK

Follow the instructions [here](https://www.ibm.com/support/pages/installing-qradar-app-sdk#:~:text=Installation%20Steps,zip%20has%20been%20extacted%20to.)

That's all for setting up the development environment.

## App development workflow

### Background 

Before we get into this, here's a bare minimum understanding of how QRadar Apps work.

QRadar Apps are independent web apps usually flask apps. They are deployed on QRadar App Host. In our case, it's the QRadar instance we've setup. Behind the scenes, the Apps are run as docker containers. The QRadar instance proxies the requests to the Apps. The Apps also allow us to deploy custom UI components which can be used in the QRadar GUI.

Following are some common workflows during development

### Quick Testing only the web service

After making some changes to the App, we can test it directly on the development instance without deploying it to the QRadar instance.

Run the following command from the project root:

```bash
qapp run -d 
```

This will start the flask app. You can navigate to it by navigating to `http://localhost:<port>`. The port is mentioned in the output of the above command.

Any changes made to the code will be reflected in the running app.

### Cleanup existing App deployments

Ignore if this is the first time you're deploying the app.

ssh into the QRadar instance and run the following command to start the App Manager wizard:

```bash
sudo /opt/qradar/support/qappmanager
```

- Type "14" and hit Enter to delete App definition.

- Select the ID of the authorized service you created earlier and hit Enter.

- Select the ID of the existing deployed version of our App and hit Enter.

### Quick Testing of the web service and QRadar GUI

Follow the "Cleanup existing App deployments" section first if relevant.

You can deploy the app to QRadar instance and test it in the GUI. This is useful when you want to test the UI components like right-click action.


#### Deploying the App

Run the following command from the project root:

```bash
make dev-package
```

This packages the app into a `CrowdSec.zip` file in the current directory.

Then navigate QRadar console on the browser. Open the QRadar App Editor App, which we installed earlier. Click on `Existing App` and upload the `CrowdSec.zip` file. 

Refresh the QRadar page and now our App should be deployed.

### Testing the App before publishing

Follow the "Cleanup existing App deployments" section first if relevant.

Make sure you've "signingstore.jks" and "signingstore_old.jks" files in the project root. These are used for signing the App.

Run the following command from the project root, Make sure to replace the `STORE_PASS` with the password for the signingstores:

```bash
STORE_PASS=password_for_signingstore make package
```

This will create a package `CrowdSec.zip` in the current directory. It'll be signed. This file can be uploaded to X-Force Exchange for publishing after validation.

You can install it on the QRadar instance via the Extension Management tool in the Admin section of the QRadar console.

You can also validate the App by uploading it to QRadar Pre-Validation App. This will output a report which can be provided to the X-Force Exchange team for publishing the App.

### Creating a new release

Before cutting a new release, update the version in the `manifest.json` and `manifest.txt` files.

There's a Github action which automatically creates the package for the App, signs it and uploads it as a release asset. This release asset can be downloaded and uploaded to X-Fore Exchange for publishing.

## References

These are some useful links which are helpful for development.

- [Sample App Repo](https://github.com/IBM/qradar-sample-apps)
- [Framework Guide PDF](https://www.ibm.com/docs/en/SS42VS_SHR/pdf/b_qradar_appframework_devguide.pdf)