# Get similar images

![](https://habrastorage.org/webt/5v/aj/x3/5vajx3dlf6fh8nnikka17wz_foc.jpeg)

This tool is a wrapper over an API that returns URLs and similarity scores for similar images for a given image.

You can find a demo of the tool [here](https://ternaus.com/).

The description of the API can be found [here](https://ternaus.com/api).

## Installation

```bash
pip install -U getsimilar
```

## Get an API token

* Log in at: [https://ternaus.com/login](https://ternaus.com/login)
* Go to the account page: [https://ternaus.com/account](https://ternaus.com/account)
* Generate new token and save json file with it to `~/.ternaus/ternaus.json`

## Usage

You pass:

* Image in the form of the `numpy` array or `PIL` image.
* URL to the image:
* Text query, for example: "Girls in weird hats"

#### Optional parameters:

* `num_similar` that specifies the number of similar images to return. This number is capped at 50. If you would like to
  get more similar images per request, please contact us
  at [https://www.ternaus.com/#contact](https://www.ternaus.com/#contact). default value is 1.
* `get_labels` that specifies whether to return labels for the image. default value is None. Right now
  only `coco_yolov7` is supported.`

### From image

```python
from getsimilar.get import from_image

urls = from_image( < numpy or PIL
image >, num_similar = < the
number
of
similar
images >)
```

### From URL

```python
from getsimilar.get import from_url

urls = from_url(url, num_similar= < the
number
of
similar
images >)
```

### From text

```python
from getsimilar.get import from_text

urls = from_text(text, num_similar= < the
number
of
similar
images >)
```
