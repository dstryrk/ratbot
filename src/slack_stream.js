var slack = require('slack-client');

var token = '<your token>';
var rtm = new slack.RtmClient(token);
rtm.start();

rtm.on(slack.RTM_EVENTS.MESSAGE, function (message) {
  console.log(message.text);
});
