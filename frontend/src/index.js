import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import './index.css';

import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider,
} from "@apollo/client";

import createUploadLink from "apollo-upload-client/createUploadLink.mjs";

const client = new ApolloClient({
  link: createUploadLink({ uri: "http://localhost:8000/graphql/" }),
  cache: new InMemoryCache(),
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>
);