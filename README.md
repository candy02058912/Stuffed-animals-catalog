# Stuffed Animals Catalog
Catalog of stuffed animals

## Screenshots
![Catalog Page](https://i.imgur.com/UbhmvNg.png)
![Pikachu](https://i.imgur.com/pvMxWOG.jpg)

## Getting Started

Prerequisites:
* Virtual box 5.1
* Vagrant 2.1.2
* FSND Vagrant Configuration: https://github.com/udacity/fullstack-nanodegree-vm

1. After installing Virtual box and Vagrant, clone the FSND vagrant configuration repo.
```
git clone https://github.com/udacity/fullstack-nanodegree-vm
```
2. Then go into the directory where the `Vagrantfile` is.
```
cd fullstack-nanodegree-vm/vagrant
```
3. Run:
```
vagrant up
```
4. After `vagrant up` has finished, run:
```
vagrant ssh
```
5. Copy the project folder `Stuffed-animals-catalog/` into `/vagrant` and run:
```
cd /vagrant/Stuffed-animals-catalog/
```
6. Setup the database:
```
python database_setup.py
```
7. Initialize the database with some items:
```
python database_initialize.py
```
8. Setup environment variables, run:
```
export SECRET_KEY=secret_key_of_your_choice
```
9. Unzip client_secrets.zip, password is in the `Submission Details` section on Udacity.
Please make sure the unzipped file is called client_secrets.json.
10. Run application:
```
python application.py
```
