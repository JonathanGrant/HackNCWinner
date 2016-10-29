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

var TestText = React.createClass({
  getInitialState: function() {
    return {
      x: 0,
      y: 0,
      z: 0,
      myText: "Motherfuckers talkin shit til you show up where they live"
    }
  },
  render: function() {
    return (<a-entity text={"text: " + this.state.myText} position="0 0 -5" scale="1 1 2"></a-entity>)
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
        <TestText />
      </a-scene>)
  }
})

ReactDOM.render(<AFrameScene />, document.getElementById('container'))