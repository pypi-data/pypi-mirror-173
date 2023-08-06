# Earlybyte Url Shortener (usage with api key only)

This tool makes it easy to use the Earlybyte linke shortener, to us this a valid api key is required.

Check the clickup for how to get the api key: https://app.clickup.com/4519779/v/dc/49xv3-428/49xv3-26847

### Installation

To run this tool Python 3.7 is required.

You might need to upgread your pip environment first before installing eb-short.

```shell
pip install --upgrade pip
```

The tool can then be installed using the following command:

```shell
pip install eb-short
```

### Usage

The tool can be used as follows:

```shell
# add an api key to the configuration (~/.eb-config.json)
eb-short add-key "<key>"

# shorten a link
eb-short short "<url>"
```

### About Earlybyte

Earlybyte GmbH is a software company from Winterthur Switzerland. We build IoT, mobile and web applications and solutions that help freeing up time for what really matters.

Find us under https://earlybyte.ch/
