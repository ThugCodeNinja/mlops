pipeline{
    agent any

    environment {
        VENV_DIR = 'venv1'
        GCP_PROJECT = "my-project-1705665346715"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/ThugCodeNinja/mlops.git']])
                }
            }
        }

        stage('Setting up our Virtual Environment and Installing dependancies'){
                steps{
                    script{
                        echo 'Setting up our Virtual Environment and Installing dependancies............'
                        sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                        '''
                    }
                }
            }

    }
}
