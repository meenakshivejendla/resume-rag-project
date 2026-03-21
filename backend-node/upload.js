const express = require("express");
const multer = require("multer");
const axios = require("axios");

const router = express.Router();

const storage = multer.diskStorage({
 destination: "uploads/",
 filename: (req, file, cb) => {
   cb(null, file.originalname);
 }
});

const upload = multer({ storage });

router.post("/", upload.fields([
 { name: "resume" },
 { name: "jd" }
]), async (req, res) => {

 const resume = req.files.resume[0].path;
 const jd = req.files.jd[0].path;

 const response = await axios.post(
   "http://localhost:8000/process",
   { resume, jd }
 );

 res.json(response.data);
});

module.exports = router;