# Simple Git GUI network configuration backup with alerts for Cisco IOS, NxOS, ASA, Arista OS, FortiOS and F5

Complete network backup setup with Ansible, Python3, Gogs (local GitHub like GUI), and alerts via Slack and/or eMail.
 
- The master Playbook ``netconfig-backup.yml`` imports the Playbooks to do everything.

- Each Playbook store the configuration files locally and optionally on Gogs. *(check Optional Setup)*

Check the short video<br/>
[![Check the short video](https://img.youtube.com/vi/_ncRyy5Spqk/0.jpg)](https://www.youtube.com/watch?v=_ncRyy5Spqk)

- **Local backup**:
    - Will get and store de configuration files in the ``./backup`` directory, with format "hostname-date-time".

    - Will only store the configuration if it's different from the last backup. *(NA for F5)*

    - By default keeps a historic of 10 configuration files. *(check Optional Setup)*
    
    - Later you can use Linux command ``diff file1 file2`` to see the configuration differences between files.

- With **Gogs backup** you don't have a limit of historic configuration files and you can easily navigate the changes in the GUI.

- Can send an email or Slack message when the backup task is complete and if a configuration backup fail per device. *(check Optional Setup)*

## Requirements
- Ansible
- Python3
- Docker
- Gogs on Docker
- pyFG (if using FortiOS)

## Setup
- Customize the ``hosts`` file according to your needs. *(Sample file provided)*.

Pay special attention to setup the ``platform=xxx`` value of each host.

According the groups you defined in the ``hosts`` file, create files with the exact name at the directory ``./group_vars``. *(Sample file provided)*.

Inside those file specify your devices credentials.

- Customize the credentials, mail, and Slack details in the files located at ``group_vars`` directory 
- If you will use Gogs:
    - Deploy the docker version of Gogs in a couple of minutes:
      1. Install docker with ``sudo apt install docker.io``
      2. Pull Gogs image with ``sudo  docker pull gogs/gogs``
      3. Make a link from the docker image to your actual operating system so you can customize the Gogs ini config: ``sudo mkdir -p /var/gogs``
      
    - Start the container <br/>
    `sudo docker run --name=gogs -p 1022:22 -p 1080:3000 -v /var/gogs:/data gogs/gogs`
    - Open a web browser and navigate to `http://localhost:1080`
    - Complete the web configuration of Gogs:
      1. Database type `SQLite3`
      2. Domain `your_Server_hostname or IP_address`
      3. SSH port `1022`
      4. Application URL `your_Server_hostname or IP_address:1080`
      5. In optional configuration add the admin account
    
## Usage

Run the master Playbook with: ``ansible-playbook netconf-backup.yml``

### Optional Setup

- It's recommended to use **Ansible-Vault** to hide the user/password and other sensible information in the files at ``group_vars`` directory.
 Check this quick guide https://adriangiacometti.net/index.php/2020/04/05/quick-start-ansible-vault/
 
- To modify the number of historic file to keep locally change that variable ``historic_files_to_keep`` in the master Playbook ``netconfig-backup.yml``.

- If you want the alerts to be sent when a configuration backup fail, set to **"yes"** the variables .
"alert_mail" and/or "alert_slack" and/or "Gogs" at the master Playbook ``netconfig-backup.yml``. And set your mail details and/or Slack webhook and/or Gogs credentials at the
file ``group_vars/all.yml``.

- If you are going to synchronize the configuration backups with Gogs:
    - Remember to never manually modify the configuration files in the directory ``backups/gogs-staging``.
    - Set you user parameters with ``git config --global user.name "FIRST_NAME LAST_NAME"`` and 
    ``git config --global user.email "MY_NAME@example.com"``
    - Then you have to create the local repository, go the ``backups/gogs-staging`` directory and type ``git init``.
    - Add some file to the directory and add it to Git staging area with ``git add .``.
    - Create a first commit to initialize the repo with ``git commit -m "first commit"``.
    - Go to Gogs and create the repository ``backups`` or the name you want for it.
    - Set it as PRIVATE and the end it will give you a Git URL.
    - Now link your local repository with the remote that you've just created with ``git remote add origin <remote_repo_url>``.
    - Set the repo URL in the configuration section of the main playbook ``netconf-backup.yml``.
    - Add the Gogs docker to systemd to easy management (autostart, restart, etc). Follow this guide
    https://mehmandarov.com/start-docker-containers-automatically/
    
- Add periodic execution via ``crontab -e``. With something like 
``0 2 * * * ansible-playbook /your_path_to/netconf-backup.yml``
for everydayexecution at 2 AM.

- If you want to integrate the messages from Gogs into Slack:
    - Get the webhook from Slack, and from the channel you want to publish the changes
    - Go to your repo in Gogs, then Setting->WebHook and add new webhook

- If you are going to backup FortiOS, you have to enable SCP with `config system global set admin-scp enable end`

### Special SSH connectivity notes

If normal prompt ssh connection don't work, it will not work with Ansible either. So first check 
the normal ssh connection from command line, and if you have problems, check these
two configurations to add to your Linux.

- Depending on the OS of your network devices you might need to enable other SSH parameters.
lines with ``sudo vi /etc/ssh/ssh_config``.

``` 
#Legacy changes
KexAlgorithms diffie-hellman-group1-sha1,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group14-sha1
Ciphers aes128-cbc,aes128-ctr,aes256-ctr
```

- On the Ansible side, analyse the addition of these two parameters in your ``.ansible.cfg``.

```
[defaults]
# uncomment this to disable SSH key host checking
host_key_checking = False

[paramiko_connection]
# When using persistent connections with Paramiko, the connection runs in a
# background process.  If the host doesn't already have a valid SSH key, by
# default Ansible will prompt to add the host key.  This will cause connections
# running in background processes to fail.  Uncomment this line to have
# Paramiko automatically add host keys.
host_key_auto_add = True
```
