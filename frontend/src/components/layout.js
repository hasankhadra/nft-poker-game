
import React from "react";
import Header from "./header";
import Footer from './footer';

import { Helmet } from "react-helmet";

function Layout(props) {
    return (
        <React.Fragment>
            <Header />
            <main style={{width: "100vw", justifyContent: "center", alignItems: "center", paddingTop: ".3rem"}} >
                {props.children}
            </main>
            <Footer />
        </React.Fragment>
    );
}

export default Layout;
