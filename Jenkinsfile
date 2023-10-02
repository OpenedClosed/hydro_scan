pipeline {
    agent any
    parameters {
        string(name: 'DJANGO_SUPERUSER_EMAIL', defaultValue: 'admin@example.com', trim: true, description: '')
        string(name: 'POSTGRES_HOST', defaultValue: 'db', trim: true, description: '')
        string(name: 'POSTGRES_PORT', defaultValue: '5432', trim: true, description: '')
        string(name: 'POSTGRES_DB', defaultValue: 'hydro_scan', trim: true, description: '')
        string(name: 'DOMAIN', defaultValue: 'new.hydroscan.ru', trim: true, description: '')
        string(name: 'PROD_FOLDER', defaultValue: 'myproject', trim: true, description: '')
    }
    environment {
        DJANGO_SECRET_KEY = credentials('DJANGO_SECRET_KEY')
        DJANGO_ADMIN_AUTH = credentials('DJANGO_ADMIN_AUTH')
        POSTGRES_ADMIN_AUTH = credentials('POSTGRES_ADMIN_AUTH')
    }
    stages {
        stage('Create env file') {
            steps {
                sh '''
                    echo 'DEBUG=0' > ./prod.env
                    echo 'DOLLAR=$' >> ./prod.env
                    echo 'SECRET_KEY'=$DJANGO_SECRET_KEY >> ./prod.env
                    echo 'DJANGO_SUPERUSER_EMAIL'=$DJANGO_SUPERUSER_EMAIL >> ./prod.env
                    echo 'DJANGO_SUPERUSER_USERNAME'=$DJANGO_ADMIN_AUTH_USR >> ./prod.env
                    echo 'DJANGO_SUPERUSER_PASSWORD'=$DJANGO_ADMIN_AUTH_PSW >> ./prod.env
                    echo 'POSTGRES_USER'=$POSTGRES_ADMIN_AUTH_USR >> ./prod.env
                    echo 'POSTGRES_PASSWORD'=$POSTGRES_ADMIN_AUTH_PSW >> ./prod.env
                    echo 'POSTGRES_HOST'=$POSTGRES_HOST >> ./prod.env
                    echo 'POSTGRES_PORT'=$POSTGRES_PORT >> ./prod.env
                    echo 'POSTGRES_DB'=$POSTGRES_DB >> ./prod.env
                    echo 'DOMAIN'=$DOMAIN >> ./prod.env
                '''
            }
        }
        stage('Stop service') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ssh_prod', keyFileVariable: 'privkey', passphraseVariable: '', usernameVariable: 'user')]) {
                    sh "ssh -o StrictHostKeyChecking=no -i ${privkey} ${user}@${DOMAIN} 'mkdir -p /root/${PROD_FOLDER}'"
                    sh "ssh -o StrictHostKeyChecking=no -i ${privkey} ${user}@${DOMAIN} 'cd /root/${PROD_FOLDER} ; if [ -f prod.yml ]; then docker compose -f prod.yml down; fi'"
                    sh "ssh -o StrictHostKeyChecking=no -i ${privkey} ${user}@${DOMAIN} 'cd /root/${PROD_FOLDER} ; if [ -f prod.yml ]; then docker volume rm -f prod_front_data; fi'"
                    sh "ssh -o StrictHostKeyChecking=no -i ${privkey} ${user}@${DOMAIN} 'rm -fr /root/${PROD_FOLDER}/*'"
                }
            }
        }

        stage('Upload files') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ssh_prod', keyFileVariable: 'privkey', passphraseVariable: '', usernameVariable: 'user')]) {
                    sh '''
                          sftp -o StrictHostKeyChecking=no -i ${privkey} ${user}@${DOMAIN} <<EOF
                          cd ${PROD_FOLDER}
                          put -r frontend
                          put -r backend
                          put -r proxy
                          put *.yml
                          put *.env
                          bye
                          EOF
                       '''
                }
            }
        }

        stage('Start service') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ssh_prod', keyFileVariable: 'privkey', passphraseVariable: '', usernameVariable: 'user')]) {
                    sh "ssh -o StrictHostKeyChecking=no -i ${privkey} ${user}@${DOMAIN} 'cd /root/${PROD_FOLDER} ; docker compose -f prod.yml up -d --build'"
                }
            }
        }
    }
}
