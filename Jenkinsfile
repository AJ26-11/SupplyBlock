pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        GIT_COMMIT = ''
    }

    stages {
        stage('Test Ganache Connection') {
            steps {
                script {
                    sh '''
                    echo "Testing connection to Ganache..."
                    curl http://localhost:7545
                    '''
                }
            }
        }
        stage('Clone Repository') {
            steps {
                script {
                    GIT_COMMIT = sh(script: "git rev-parse HEAD", returnStdout: true).trim()
                    git url: 'https://github.com/AJ26-11/SupplyBlock.git', branch: 'main'

                }
            }
        }
        stage('Run Unit Tests Locally') {
            steps {
                sh 'python3 manage.py test'
            }
        }
        stage('Build Docker Image') {
    steps {
        echo "Building Docker Image with tag elliot1022/coffeechain:${GIT_COMMIT}"
        sh "docker build -t elliot1022/coffeechain:${GIT_COMMIT} ."
    }
}

        stage('Run Tests in Docker') {
            steps {
                sh "docker run elliot1022/coffeechain:${GIT_COMMIT} python3 manage.py test"
            }
        }
        stage('Push to Docker Hub') {
    steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USERNAME')]) {
            sh "echo '${DOCKERHUB_PASSWORD}' | docker login -u '${DOCKERHUB_USERNAME}' --password-stdin"
            sh "docker push elliot1022/coffeechain:${GIT_COMMIT}"
            sh "docker logout"
        }
    }
}

        stage('Run Selenium Tests') {
            steps {
                sh 'python3 selenium_tests.py'
            }
        }
    }

    post {
        failure {
            emailext (
                subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "A build has failed. Check Jenkins for details.",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']],
                to: 'aryan.bhasein20@st.niituniversity.in'
            )
        }
        success {
            mail to: 'aryan.bhasein20@st.niituniversity.in',
                 subject: "SUCCESS: Jenkins Build #${env.BUILD_NUMBER}",
                 body: "Commit: ${GIT_COMMIT}\nBuild Status: ${currentBuild.currentResult}\nCheck Jenkins for more details."
        }
        always {
            // Clean up Docker images and containers
            sh 'docker rmi $(docker images -q elliot1022/coffeechain) --force'
            sh 'docker rm $(docker ps -a -q) --force'
        }

    }
}
