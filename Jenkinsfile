// Multibranch Pipeline: Jenkins runs this file for every branch and PR.
pipeline {

    // Build inside a Python container so the agent needs only Docker.
    // (No Docker? Replace with `agent any` and make sure python3 + venv exist.)
    agent {
        docker {
            image 'python:3.12-slim'
            args  '-u root:root'   // simple default; see README for non-root setup
        }
    }

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
        disableConcurrentBuilds(abortPrevious: true)
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    environment {
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        VENV = "${WORKSPACE}/.venv"
    }

    stages {

        stage('Setup') {
            steps {
                sh '''
                    python -m venv "$VENV"
                    . "$VENV/bin/activate"
                    pip install -r requirements-dev.txt
                    pip install -e .
                '''
            }
        }

        stage('Quality') {
            parallel {
                stage('Lint') {
                    steps {
                        sh '. "$VENV/bin/activate" && flake8 src tests'
                    }
                }
                stage('Unit tests') {
                    steps {
                        sh '''
                            . "$VENV/bin/activate"
                            mkdir -p reports
                            pytest --junitxml=reports/junit.xml \
                                   --cov=textutils \
                                   --cov-report=xml:reports/coverage.xml \
                                   --cov-report=html:reports/htmlcov
                        '''
                    }
                    post {
                        always {
                            junit 'reports/junit.xml'
                        }
                    }
                }
            }
        }

        stage('Build package') {
            steps {
                sh '. "$VENV/bin/activate" && python -m build'
            }
        }

        // Runs only for pull requests (multibranch exposes CHANGE_ID for PRs)
        stage('PR checks') {
            when { changeRequest() }
            steps {
                echo "Pull request #${env.CHANGE_ID}: ${env.CHANGE_BRANCH} -> ${env.CHANGE_TARGET}"
            }
        }

        // Only the main branch gets deployed
        stage('Deploy') {
            when { branch 'main' }
            steps {
                echo 'Deploying to staging...'
                // Example: publish to an internal package index
                // withCredentials([usernamePassword(credentialsId: 'pypi-internal',
                //         usernameVariable: 'TWINE_USERNAME',
                //         passwordVariable: 'TWINE_PASSWORD')]) {
                //     sh '. "$VENV/bin/activate" && pip install twine && twine upload --repository-url https://pypi.example.com/ dist/*'
                // }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'dist/*, reports/**', allowEmptyArchive: true
        }
        success { echo "Branch ${env.BRANCH_NAME} built successfully." }
        failure { echo "Branch ${env.BRANCH_NAME} failed. Check the console output." }
        cleanup { cleanWs() }
    }
}
