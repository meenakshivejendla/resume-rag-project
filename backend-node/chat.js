const express = require("express");
const axios = require("axios");

const router = express.Router();

router.post("/", async (req, res) => {

 const question = req.body.question;

 const response = await axios.post(
   "http://localhost:8000/chat",
   { question }
 );

 res.json(response.data);
});

module.exports = router;