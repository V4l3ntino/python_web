const router = require("express").Router();
const { jsonResponse } = require("../lib/jsonResponse");


router.post("/", (req, res) => {
    const {username, name, password} = req.body;

    if(!!!username || !!!name || !!!password){
        return res.status(400).json(jsonResponse(400, {
            error:"Fields are required",
        }))
    }


    //crear usuario en la base de datos

    res
       .status(200)
       .json(jsonResponse(200, {message: "User created succesfully"}))

    res.send("signout");
})

module.exports = router;