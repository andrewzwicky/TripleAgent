|icon| Triple Agent |py_version| |platform| |license| |build_status| 
========================================================
Triple Agent is a utility to parse and analyze the timeline component of SpyParty replays. [1]_  The Triple Agent repository also contained pre-parsed games from recent Spy Party competitive events that can be analyzed without spending the time to parse.

Triple Agent works by automatically scrolling and taking screenshots of the timeline of games, but *is not able to directly read timeline content from replay files at this time*.  This means that parsing does require a computer with SpyParty installed, and may not work will all setups currently. [1]_.  Once the screenshots are taken, optical character recognition (OCR) is used to extract the relevant information and store it as a python object so it can be analyzed.

Available Data
______________
Available data includes anything that can be seen directly from the timeline including:

- Timeline event text
- Timeline event times
- Cast data
- Partial mission progress

This excludes:

- Spatial data (time add locations, which statues are swapped most, etc.)
- Animation data (starting statue layout, number of read animations, idle times, etc.)

Examples
________
The examples_ folder showcases some of the most interesting or useful statistics that can be obtained with this data.

Basic Usage
___________
This repo contains serialized files for all the replays covering SCL4, SCL5, Winter Cup 2019, Summer Cup 2019.


Installation
____________
You'll need to have `Python 3.7`_ installed (untested with other versions of python).

The most basic usage for Triple Agent is plotting the included replays.  To do this run ``pip install -e .[plot]`` from the command line in the top level folder to install the necessary dependencies.

Thanks
______

* checker for making SpyParty
* LtHummus for the `SpyPartyParse`_ library.
* WarningTrack for `SpyParty Fans`_, and the competitive replay downloads, which were a major help with this project.


License
-------
This project is licensed under the MIT License - see the `LICENSE.md`_ file for details

.. [1] At this time, parsing is not fully automated and may not work for all setups, see `Parsing Quirks`_ for more information. 

.. _SpyParty: http://www.spyparty.com/
.. _LICENSE.md: LICENSE.md
.. _`Python 3.7`: https://www.python.org/downloads/windows/
.. _SpyPartyParse: https://github.com/LtHummus/SpyPartyParse
.. _`SpyParty Fans`: https://www.spypartyfans.com/
.. _examples: ../tree/master/examples
.. _`Parsing Quirks`: ../wiki/Parsing-Quirks
.. |icon| image:: triple_agent/images/icons/magnifying_glass_icon.svg
  :height: 32px
  :width: 32px

.. |py_version| image:: https://img.shields.io/badge/python-3.7-blue.svg
.. |platform| image:: https://img.shields.io/badge/platform-windows--x64-blue.svg
.. |build_status| image:: https://ci.appveyor.com/api/projects/status/vrw0751wstpa6pf7?svg=true
.. |license| image:: https://img.shields.io/github/license/andrewzwicky/TripleAgent.svg?color=blue
