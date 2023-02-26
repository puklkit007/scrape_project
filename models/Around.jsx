import React from "react";
import Navbar from "./Navbar";
import OrderCard from "./OrderCard";
import Summary from "./Summary";
import item1 from "../assets/item-1.jpeg";
import item2 from "../assets/item-2.png";
import item3 from "../assets/item-3.png";
import axios from 'axios'
import { signInWithGoogle, auth, logout } from '../firebase'
import { useState, useEffect } from "react";
import GoogleMapReact from 'google-map-react';
import { useAuthState } from "react-firebase-hooks/auth";


const AnyReactComponent = ({ text }) => <div>{text}</div>;

const Around = () => {
  const [users, setUsers] = useState([]);

  const [user, loading, error] = useAuthState(auth);
  //const [signInWithGoogle, user, loading, error] = useSignInWithGoogle(auth);


  console.log(auth)

  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);
  const [count, setCount] = useState(0);

  const fetchURL = "http://localhost:4000/auth/users"
  const putURL = "http://localhost:4000/auth/update"

  const defaultProps = {
    center: {
      lat: latitude || 40.6943194,
      lng: longitude || -73.9867685
    },
    zoom: 20
  };

  useEffect(() => {
    axios.get(fetchURL).then((response) => {
      setUsers(response.data)
    })

    const interval = setInterval(() => {
      getLocation()
      // Call your function here
      setCount(prevCount => prevCount + 1);
    }, 2000); // 10 seconds in milliseconds

    return () => clearInterval(interval);

  }, [])

  console.log(users)

  const getLocation = () => {
    if (navigator.geolocation) {


      navigator.geolocation.getCurrentPosition(position => {
        setLatitude(position.coords.latitude);
        setLongitude(position.coords.longitude);
        console.log("lok")
        {!user && axios.put(putURL, {id:user.email, lat:position.coords.latitude, long:position.coords.longitude,name:user.name})}
      }, error => {
        console.log(error);
      });
    } else {
      console.log("Geolocation is not supported by this browser.");
    }
  };

  return (
    <div className="h-full">
      <Navbar></Navbar>
      <hr></hr>
      <div>
        <div onClick={getLocation}>share my location</div>
        <div>lat:{latitude}</div>
        <div>long:{longitude}</div>
      </div>
      <div style={{ height: '100vh', width: '100%' }}>
      <GoogleMapReact
        bootstrapURLKeys={{ key: "AIzaSyBH2m3Tu82Fa7lVAfoHbjmZi0oNfgVdJfU" }}
        defaultCenter={defaultProps.center}
        defaultZoom={defaultProps.zoom}
      >
        <AnyReactComponent
          lat={latitude || 40.6943194}
          lng={longitude || -73.9867685}
          text="📍"
        />

        {users.map((users, index) => (
          <Marker
            key={index}
            lat={users.lat}
            lng={users.long}
            text={users.name}
          />
        ))}

      </GoogleMapReact>
    </div>
    </div>
  );
};


function Marker({ text }) {
  return (
    <div style={{ color: 'red', fontWeight: 'bold' }}>
      {text+"📍"}
    </div>
  );
}

export default Around;
