pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'sudo docker build . -t tournament-manager:py'
            }
        }
        stage('Remove Previous Container') {
            steps {
                sh '''
                if sudo docker ps | grep -q tournament-manager-''' + env.BRANCH_NAME + '''; then
                    sudo docker rm -f tournament-manager-''' + env.BRANCH_NAME + '''
                fi'''
            }
        }
        stage('Run') {
            steps {            
                sh 'sudo docker run --restart=always --name tournament-manager-' + env.BRANCH_NAME + ' -e token=$token -d tournament-manager:py'
            }
        }
    }
}