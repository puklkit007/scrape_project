const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const mongoose = require('mongoose');

const MongoClient = require('mongodb').MongoClient;

const authRouter = require('./routes/auth');
const accountRouter = require('./routes/account')
require("dotenv").config();


const DBURL = process.env.DBURL;
const app = express();

app.use(bodyParser.json());
app.use(cors());
app.use('/auth', authRouter)
app.use('/account',accountRouter)

const connectionParams = {
  useNewUrlParser: true,
  useUnifiedTopology: true,
};

mongoose
  .connect('mongodb+srv://hacknyu:XcTcnhyeKX5PP6b0@meta.mkvgfml.mongodb.net/?retryWrites=true&w=majority', connectionParams)
  .then(() => {
    console.log("connected to db");
  })
  .catch((err) => {
    console.log(`${err}`);
  });

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Define a schema for the data you want to save
const dataSchema = new mongoose.Schema({
  email: String,
  organization: String,
  who_are_you: String,
  interests: String,
  looking_for: String
});

// Create a model based on the schema
const Data = mongoose.model("Data", dataSchema);


// Define a route for handling form submissions
app.post("/submit", function (req, res) {
  console.log('Hi Submit')
  console.log(req.body)
  const newData = new Data({
    'email': req.body.email,
    'organization': req.body.organization,
    'who_are_you': req.body.occupation,
    'interests': req.body.interests,
    'looking_for': req.body.preferred_interests
  });
  newData.save(function (err) {
    if (err) {
      console.log(err);
      res.send("There was an error.");
    } else {
      res.send("Data saved successfully!");
    }
  });
});

// fetch data from MongodB
const url = 'mongodb+srv://hacknyu:XcTcnhyeKX5PP6b0@meta.mkvgfml.mongodb.net/?retryWrites=true&w=majority'; // Connection URL
const dbName = 'test'; // Database Name


app.get('/getData', (req, res) => {
  // Retrieve data from MongoDB database
  Data.find({}, (err, getData) => {
    if (err) {
      console.error(err);
    } else {
      // Render HTML page with retrieved data
      res.render('secondPage', { getData: getData });
    }
  });
});

app.listen(process.env.PORT || 4000, () => console.log(`Started server`));
