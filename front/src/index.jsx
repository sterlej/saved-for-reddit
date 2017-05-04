import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux'
import { AppContainer } from 'react-hot-loader';
import App from './app.jsx';
import storeFactory from './store'

const store = storeFactory()

window.React = React
window.store = store

render( <AppContainer>

          <Provider store={store}>
              <App />
          </Provider>

	</AppContainer>, document.querySelector("#app"));

if (module && module.hot) {
  module.hot.accept('./app.jsx', () => {
    const App = require('./app.jsx').default;
    render(
      <AppContainer>

        <Provider store={store}>
            <App />
        </Provider>

      </AppContainer>,
      document.querySelector("#app")
    );
  });
}

