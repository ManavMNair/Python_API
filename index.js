var express = require('express');
var router = express.Router();
const axios= require('axios')

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});
  
  // Add more modifications as needed

  router.post('/get-summary', async(req,res)=> {
    res.render('index',{isDisabled : true});

    const youtube_video = req.body['youtube-link'];
    console.log(youtube_video);
  
    // Make an HTTP request to your Python API using axios
    try{
      const response = await axios.post('http://127.0.0.1:5000/get-summary', {youtube_video})
      const text = response.data;
      res.render('index', { isDisabled: false, text: text });
    } catch (error){
      console.error('Error  : ',error);
      res.status(500)
      res.render('index', { isDisabled: false, text: '' }); // Handle the error case
    

    }});


        
   

module.exports = router;
