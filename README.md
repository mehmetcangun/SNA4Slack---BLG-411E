### GROUP 22
## BLG 411E - Software Engineering Project - [`Based on SCORE PROJECT`](http://score-contest.org/2018/projects/sna4slack.php)
#### SNA4Slack | Social Network Analysis for Slack Teams 

## [`Presentation`](https://docs.google.com/presentation/d/1oIC0xy6BVvCiCfKAbrICXVUR4zrisTtVDCw-ttqgdlg/edit?usp=sharing)

## [`Demo Video`](https://drive.google.com/file/d/1Du5Xg8NC4cth4cBuhe-hCCNgeaLYKBhY/view?usp=sharing)

## Team
- Muhammed Salih Yıldız
- Ömer Faruk Topal
- Emre Çağıran
- Mehmet Can Gün

## Tech
- Python3
- Flask
- NetworkX
- SQLAlchemy - PostgreSQL
- Front-End: Bootstrap 4, Chart.js
- Deployment: Heroku

## Installation
> Download repository and extract to the folder as group22 either using git clone.

```sh
git clone https://github.com/itusweng/group22.git
```
> Change directory to group22 folder.

```sh
cd group22
```
> Following command to create environment as demo_env.

```sh
python3 -m venv demo_env
```
> Activate demo_env environment.

```sh
source demo_env/bin/activate
```
> Install requirements for the app.

```sh
pip3 install -r requirements.txt
```
> Run the following command to run app.

```sh
gunicorn server:app
```
> Enter the localhost link given with gunicorn command.

```sh
http://127.0.0.1:8000
```
