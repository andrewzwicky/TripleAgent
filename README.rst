|icon| Triple Agent |py_version| |platform| |license| |build_status| 
========================================================
Triple Agent is a utility to parse and analyze the timeline component of SpyParty replays. [1]_  The Triple Agent repository also contained pre-parsed games from recent Spy Party competitive events that can be analyzed without spending the time to parse.

Triple Agent works by automatically scrolling and taking screenshots of the timeline of games, but *is not able to directly read timeline content from replay files at this time*.  This means that parsing does require a computer with SpyParty installed, and may not work will all setups currently. [1]_.  Once the screenshots are taken, optical character recognition (OCR) is used to extract the relevant information and store it as a python object so it can be analyzed.

Available Data
______________

- Timeline event text
- Timeline event times
- Cast data
- Partial mission progress

Basically, if you can see it in the timeline, it's available!

Unavailable Data
________________

- Spatial data (time add locations, which statues are swapped most, etc.)
- Visual data (starting statue layout, number of read animations, idle times, etc.)

Basically, if you couldn't see it by reading the timeline as text, it's unavailable!

Basic Usage
___________
This repo contains serialized files for all the replays covering SCL4, SCL5, Winter Cup 2019, Summer Cup 2019.


Installation
____________
You'll need to have `Python`_ (3.7.3 or greater) installed.

The most basic usage for Triple Agent is plotting the included replays.  To do this run ``pip install -e .[plot]`` from the command line in the top level folder to install the necessary dependencies.

Thanks
______

* checker for making SpyParty
* LtHummus for the [SpyPartyParse](https://github.com/LtHummus/SpyPartyParse) library.
* WarningTrack for [SpyParty Fans](https://www.spypartyfans.com/), and the competitive replay downloads, which were a major help with this project.


License
-------
This project is licensed under the MIT License - see the `LICENSE.md`_ file for details

.. [1] At this time, parsing is not fully automated and may not work for all setups, see parsing caveats for more information. 

.. _SpyParty: http://www.spyparty.com/
.. _LICENSE.md: LICENSE.md
.. _Python: https://www.python.org/downloads/windows/
.. |icon| image:: triple_agent/images/icons/magnifying_glass_icon.svg
  :height: 32px
  :width: 32px

.. |py_version| image:: https://img.shields.io/badge/python-3.7-blue.svg
.. |platform| image:: https://img.shields.io/badge/platform-windows--x64-blue.svg
.. |build_status| image:: https://ci.appveyor.com/api/projects/status/vrw0751wstpa6pf7?svg=true
.. |license| image:: https://img.shields.io/github/license/andrewzwicky/TripleAgent.svg?color=blue
