const express = require('express')
const router = express.Router()
const Auth = require('../models/auth')

router.post('/register', async (req,res) => {
    const newAuth = new Auth({
        _id: req.body.email, 
        lat: req.body.lat, 
        long: req.body.long, 
        name: req.body.name
    }) 

    console.log(newAuth); 
    try{
        const newUser = await newAuth.save()
        res.send(JSON.stringify("user registered"))
    } catch (err){
        res.sendStatus(500).json({message: "user exist"})
    }
})

router.get("/users", async (req, res) => {
    try{
        const users = await Auth.find()
        res.json(users)
    } catch(err) {
        res.sendStatus(500).json( {message: err.message})
    }
})

router.get("/:id", async (req, res) => {
    try{
        const user = await Auth.findById(req.params.id)
        res.json(user)
    }catch(err){
        res.status(500).json( {message: err.message})
    }
})

router.put("/update", async(req, res) => {
    let user = await Auth.findById(req.body.id)
    console.log(user)
    user.lat = req.body.lat
    user.long = req.body.long
    try{
        const updatedAccount = await user.save()
        res.json(updatedAccount)
    }catch(err){
        res.status(400).json({message: err.message})
    }
})

module.exports = router