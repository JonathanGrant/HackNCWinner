var Camera = React.createClass({
  getInitialState: function() {
    return {
      pos: '0 0 0'
    }
  },
  render: function() {
    return (
        <a-camera position={this.state.pos}>
            <a-cursor color="#FF0000"></a-cursor>
        </a-camera>
        )
  }
})

var Sky = React.createClass({
  render: function() {
    return (<a-sky src="./src/img/sky.jpg"></a-sky>)
  }
})

var AFrameScene = React.createClass({
  getInitialState() {
    return {
      restart: false
    }
  },
  render: function() {
    return (
      <a-scene>
        <Camera />
        <Sky />
      </a-scene>)
  }
})

ReactDOM.render(<AFrameScene />, document.getElementById('container'))