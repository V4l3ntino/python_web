const router = require("express").Router();
const { jsonResponse } = require("../lib/jsonResponse");
const User = require("../schema/user");
const getUserInfo = require("../lib/getUserInfo");


router.post("/", async(req, res) => {
    const {username, password} = req.body;

    if(!!!username || !!!password){
        return res.status(400).json(jsonResponse(400, {
            error:"Fields are required",
        }))
    }

    const user = await User.findOne({ username });

    if(user){
        const correctPassword = await user.comparePassword(password, user.password);

        if(correctPassword){
                //autenticar usuario
            const accessToken = user.createAccessToken();
            const refreshToken = await user.createRefreshToken();
            // const user = {
            //     id: "1",
            //     name: "John De",
            //     username: "xxxxxx",
            // };
            res
            .status(200)
            .json(jsonResponse(200, { user: getUserInfo(user), accessToken, refreshToken }))
        }else{
            res.status(400).json(
                jsonResponse(400, {
                    error: "User or password icorrect",
                })
            )
        }
    }else{
        res.status(400).json(
            jsonResponse(400, {
                error: "User not found",
            })
        )
    }



});

module.exports = router;