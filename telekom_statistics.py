# -*- coding: utf-8 -*-
"""Script to ask pass.telekom.de for the current usage statistic"""
import json
import urllib.request
import urllib.error

PASS_HOST = "pass.telekom.de"
API_ENDPOINT = f"https://{PASS_HOST}/api/service/generic/v1/status"


def generate_text() -> str:
    """Output mimicking PASS_HOST. See https://docs.xfce.org/panel-plugins/xfce4-genmon-plugin/start for styling information"""
    connected: bool
    api_answer: dict = {}
    try:
        with urllib.request.urlopen(API_ENDPOINT) as telekom_api:
            api_answer = json.load(telekom_api)
            connected = True
    except (json.decoder.JSONDecodeError, urllib.error.URLError):
        # if the output can't be decoded, that means we don't have access to the API and are not in the Telekom mobile network.
        connected = False
        api_answer["icon"] = "network-wireless-disconnected"
        api_answer["availableVolumePercent"] = 0
        api_answer["initialVolume"] = 1
        api_answer["usedVolume"] = 0
    # convert the nested dict to an object
    api_answer["initialVolumeShort"] = api_answer["initialVolume"] / 1024**3
    api_answer["usedVolumeShort"] = api_answer["usedVolume"] / 1024**3
    api_answer["remainingVolumeShort"] = (
        api_answer["initialVolume"] - api_answer["usedVolume"]
    ) / 1024**3
    api_answer["availableVolumePercent"] = (
        1 - api_answer["usedVolume"] / api_answer["initialVolume"]
    ) * 100

    api_answer["icon"] = "network-wireless-connected-00"
    api_answer["colour"] = "red"
    if api_answer["availableVolumePercent"] >= 25:
        api_answer["icon"] = "network-wireless-connected-25"
        api_answer["colour"] = "orange"
    if api_answer["availableVolumePercent"] >= 50:
        api_answer["icon"] = "network-wireless-connected-50"
        api_answer["colour"] = "yellow"
    if api_answer["availableVolumePercent"] >= 75:
        api_answer["icon"] = "network-wireless-connected-75"
        api_answer["colour"] = "green"

    return_string: str = "<txt>Telekom</txt>"
    return_string += f"<txtclick>exo-open {PASS_HOST}</txtclick>"
    return_string += f"<icon>{api_answer['icon']}</icon>"
    return_string += f"<iconclick>exo-open {PASS_HOST}</iconclick>"
    return_string += f"<bar>{api_answer['availableVolumePercent']}</bar>"
    return_string += "<tool>"
    if connected:
        return_string += f"{api_answer['passName']}\n"
        return_string += "<small>Ihr verbleibendes Datenvolumen</small>\n\n"
        return_string += f"<span foreground='{api_answer['colour']}'>{api_answer['remainingVolumeShort']:.2f}</span>/{api_answer['initialVolumeShort']:.2f} GiB\n"
        return_string += (
            f"<small>verbleibend für {api_answer['remainingTimeStr']}</small>"
        )
    else:
        return_string += (
            "<span lang='de'>Nicht mit dem Telekom-Mobil-Netz verbunden.</span>"
        )
    return_string += "</tool>"
    return return_string


if __name__ == "__main__":
    print(generate_text())
