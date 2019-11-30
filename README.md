<h1 align="center"><a href="https://hackathonlocator.herokuapp.com">View The Demo</a></h1>

<p align="center">
<img src ="static/demo.png">
</p>

# API

## GET: /getByLongLat?lat={latitude}&long={longitude}

### ?expand=True

```javascript
Response:
[
  {
    "distance": 913.4828683815352, 
    "title": "QBHacks 2019"
  }, 
  {
    "distance": 3692.142205746163, 
    "title": "UBC Local Hack Day 2019 - Build Day: Powered by TTT Studios"
  }, 
  {
    "distance": 6553.8947994335795, 
    "title": "Hackking's 6.0"
  }, 
  {
    "distance": 15807.863121194276, 
    "title": "Accenture Hackathon - Banking Revolution Edition"
  }
]
```

Note: *distance* refers to the [Haversine Distance](https://en.wikipedia.org/wiki/Haversine_formula) between your current longitude/latitude and the reported location of the hackathon.

### ?expand=False

```javascript
Response:
QBHacks 2019
```

## License
 
The MIT License (MIT)

Copyright (c) 2015 Chris Kibble

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.