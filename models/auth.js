const mongoose = require('mongoose')

const authSchema = new mongoose.Schema({
    _id:{
        type:String, 
        required: true
    },
    lat:{
        type:String, 
        required: true, 
        default: "0"
    }, 
    long:{
        type: String, 
        required:true,
        default:"0"
    }, 
    name:{
        type:String, 
        required:true, 
        default:"name"
    }

})

module.exports = mongoose.model('user', authSchema)