const getTokenFromHeader = require("../auth/getTokenFromHeader");

const router = require("express").Router();

router.get("/", async (req, res) => {
    const refreshToken = getTokenFromHeader(req.headers);
    if(refreshToken){
        try {
            const found = await Token.findOne({ token: refreshToken })
            if(!found){
                return res
                    .status(401)
                    .send(jsonResponse(401, {error: "Unautorized"}));
            }


        } catch (error) {
            
        }
    }else{
        res.status(401).send(jsonResponse(401, {error: "Unauthorized"}))
        
    }
    res.send("refresh token")
})

module.exports = router;

//MINUTO 1:59:07