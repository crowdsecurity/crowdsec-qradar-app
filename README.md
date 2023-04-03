# CrowdSec QRadar App

QRadar App which allows users to leverage CrowdSec's Smoke CTI to get information about IP as seen by CrowdSec's network. This is enabled via a right click on IP GUI action. The intelligence includes:

1. Types of attacks the IP has been observed performing.
2. Background Noise Score. This can be used to know whether the particular IP is only targeting your infrastructure or is targeting others too. 
3. Aggressivity which quantifies frequency of attacks.
4. Other fields like Geolocation details, AS details, sighting details etc

## Configuration

We need to provide the App, CrowdSec CTI API Key. You can find the instructions to obtain it [here](https://docs.crowdsec.net/docs/next/cti_api/getting_started)

Now navigate to the CrowdSec App in QRadar's Admin page. Click on CrowdSec App Settings Icon.

![CrowdSec App Settings](/images/qradar_crowdsec_cfg.png)

A pop-up will appear. Enter the API Key and click on Submit.

![CrowdSec App Settings Popup](/images/crowdsec_app_config_window.png)

The App is now configured !

## Usage

Navigate to Log Activity pane in QRadar. Right click on an IP either in Source IP or Destination IP column. Hover over "More Options". You will see a new option "CrowdSec IP Lookup". Click on it.

![CrowdSec Right Click Option](/images/right_click_show_act.png)

This will open a popup with the information about the right clicked IP found in CrowdSec's Smoke Dataset.

![CrowdSec App Popup](/images/lookup_results.png)

You can click on the "Show" button to see the RAW JSON response from the API.

![JSON View](/images/qradar_json_view.png)

## References

You can find our latest taxonomy about attack details, classifications, scores etc in [our official docs](https://docs.crowdsec.net/docs/next/cti_api/taxonomy)



