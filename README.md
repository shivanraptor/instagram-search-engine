# Instagram Image Reverse Search Engine
This is an experimental Image Reverse Search Engine for Instagram (IG).


**Reason to create this Search Engine**

1. Instagram images are not searchable via Google Images Reverse Search
2. There is no similar IG-targeted search engine in the market

**The Mechanism**

The mechanism is simple yet ineffective at this moment.

1. Download some IG users' images via rarcega's [Instagram Scraper](https://github.com/rarcega/instagram-scraper/)
2. **Image Hashing / Perceptual Hashing**: Use Python library [ImageHash](https://pypi.org/project/ImageHash/)'s difference hash (`dhash()`) function to hash every image and save it to MySQL database.
3. When a user uploads an image to perform reverse search, the system will compare the hashes in the database and found out the answer(s); more than 1 answer might return. We only return the IG user name(s) as answer.

**Requirements and Installation**

In this project, programming language Python and MySQL database are used. The following libraries are used:

- ImageHash 4.0
- Pillow 5.3
- imutils 0.5.2
- OpenCV 3.4.5.20
- MySQL 
- MySQL Client

Note: We're using Ubuntu Server 16.04 LTS, assumed Python 2.7 and MySQL server are installed. Before installing Python libraries, the following command has to be executed in Ubuntu first (to install additional library in Ubuntu):

    sudo apt-get install libmysqlclient-dev libsm6 libxrender1 libxext6

Then, you can install these via `pip`: `pip install imagehash pillow imutils opencv-python mysqlclient`

**Usage**

*Preparation Phase - Images*
1. Download the images from IG users
2. Save it to `images/` folder, with IG user name as subfolder names. Example: if the IG user name is `abc123`, the photos should be stored at `images/abc123/`.

*Preparation Phase - Database*
1. Run the database initiation script: `db_init.sql` in MySQL

*Indexing Phase*
1. Run the indexing script: `python index.py --dataset images`
2. The script will load for few minutes, computing the hashes and store in MySQL database.

*Usage Phase*
1. To search the images, run: `python search.py --dataset images --query path/to/image_to_search.jpg`
2. The result will return.

**Problems**

1. The major problem is the Instagram Scraper Python script always return 403 Forbidden after few minutes of scraping, due to increased security measures of Instagram. Instagram will block suspecious connections if the scraping is too fast.

- To deal with this problem, we temporarily use some Chrome extension to fetch IG users' images. This approach has to be done manually, which is inefficient.

2. The next problem is the storage space. we fetched around 30 IG users' images (around 28,000 images) and 8GB is consumed. Fun fact: Each Instagram image can be as low as 19KB and can be as large as 2.2MB.

- To deal with this problem, we archived the completed images (JPEG is always efficient in archiving) and took it offline, as we only require to return the user name of the IG users. If some days later an image is required to return to user, the image will be extracted from the archive and show in the search result page.

3. Updates of IG images: The Instagram Scraper can download IG users' images incrementally via last update time, but due to the 403 Forbidden issue, the plan is no longer working. 

- Still finding a way to tackle this problem. Yet, for a prototype, it is already sufficient.

**Future Updates**

- Website version of this prototype
