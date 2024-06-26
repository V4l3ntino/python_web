import { useContext, createContext, useState, useEffect } from "react";
import { AuthResponse, AccesstokenResponse, User } from "../types/types";
import { API_URL } from "./constants";


interface AuthProviderProps{
    children: React.ReactNode;
}


const AuthContext = createContext({
    isAuthenticated: false,
    getAccessToken: () => {},
    saveUser: (userData: AuthResponse) => {},
    getRefreshToken: () => {}
})

export function AuthProvider({children}: AuthProviderProps){

    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const [accessToken, setAccessToken] = useState<string>("");

    const [user, setUser] = useState<User>();

    //const [refreshToken, setRefreshToken] = useState<string>("");

    useEffect(() => {},[]);

    async function requestNewAccessToken(refreshToken:string){
        try {
            const response = await fetch(`${API_URL}/refresh-token`,{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${refreshToken}`
                },
            });

            if(response.ok){
                const json = await response.json() as AccesstokenResponse; 
                if(json.error){
                    throw new Error(json.error)
                }

                return json.body.accessToken;

            }else{
                throw new Error(response.statusText)
            }
        } catch (error) {
            console.log(error);
            return null;
        }
    }

    async function getUserInfo(accessToken: string){
        try {
            const response = await fetch(`${API_URL}/user`,{
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${accessToken}`
                },
            });

            if(response.ok){
                const json = await response.json(); 
                if(json.error){
                    throw new Error(json.error)
                }

                return json;

            }else{
                throw new Error(response.statusText)
            }
        } catch (error) {
            console.log(error);
            return null;
        }
    }
    

    async function checkAuth(){
        if(accessToken){
            //el usuario esta autenticado

        }else{
            //el usuario no esta autenticado
            const token = getRefreshToken();
            if(token){
                const newAccessToken = await requestNewAccessToken(token);
                if(newAccessToken){
                    const userInfo = await getUserInfo(newAccessToken);
                    if(userInfo){
                        saveSessionInfo(userInfo, newAccessToken, token)
                    }
                }
            }
        }
    }

    function saveSessionInfo(userInfo:User, accessToken:string, refreshToken: string){
        setAccessToken(accessToken);   
        localStorage.setItem("token", JSON.stringify(refreshToken)); 
        setIsAuthenticated(true);
        setUser(userInfo);
    }

    function getAccessToken(){
        return accessToken;
    }
    function getRefreshToken(): string|null{
        const token = localStorage.getItem("token");
        if(token){
            const { refreshToken } = JSON.parse(token);
            return refreshToken;
        }
        return null;
    }

    function saveUser(userData: AuthResponse){
        saveSessionInfo(userData.body.user, userData.body.accessToken, userData.body.refreshToken);
    }

    return (
        <AuthContext.Provider value={{ isAuthenticated, getAccessToken, saveUser, getRefreshToken }}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => useContext(AuthContext);