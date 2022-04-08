
import React from "react";
import Header from "./header";
import Footer from './footer';

import { Helmet } from "react-helmet";

function Layout(props) {
    console.log(props)
    return (
        <React.Fragment>
            <Header />
            <main>
                {props.children}
            </main>
            <Footer />
        </React.Fragment>
    );
}

export default Layout;
