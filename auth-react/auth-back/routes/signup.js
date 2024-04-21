const router = require("express").Router();
const { jsonResponse } = require("../lib/jsonResponse");
const User = require("../schema/user");


router.post("/", async (req, res) => {
    const {username, name, password} = req.body;

    if(!!!username || !!!name || !!!password){
        return res.status(400).json(
            jsonResponse(400, {
            error:"Fields are required",
          })
        );
    }

    try {

        const user = new User();
        const exist = await user.usernameExist(username);

        if(exist){
            return res.status(400).json(
                jsonResponse(400, {
                    error: "Username already exists"
                })
            )
        }

        //crear usuario en la base de datos

        async function guardarUsuario() {
            const user = new User({
                username,
                name,
                password
            });
        
            await user.save();
        }
        guardarUsuario();
        


        res
        .status(200)
        .json(jsonResponse(200, {message: "User created succesfully"}))

        //res.send("signout");
        
    } catch (error) {
        res.status(500).json(
            jsonResponse(500, {
                error: "Error creating user"
            })
        )
    }
    
    
});

module.exports = router;