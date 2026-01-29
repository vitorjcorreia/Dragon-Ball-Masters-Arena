# Dragon-Ball-Masters-Arena

## Summary
A repository focused on leveraging Dragon Ball Super Card Game Masters to [TCG Arena](https://www.tcg-arena.fr).

## Repository Structure
The repository is organized in the following way:
* `assets`: dump of TCG Arena compatible card data and images used by the platform.
* `imgs`: tokens for helping resolve effects in gameplay and other useful assets.
* `src`: scripts to generate compatible card data with the platform and download images. When there is a new set, scripts are meant to be run.
* `cards.json`: compiled card data of every set. Updated when new sets are released.
* `Game_Dragon Ball Super Card Game_Final.json`: game file to organize gameplay and deck building in TCG Arena.

## Future Improvements

### 2026-01-29
- [ ] Automate run of the scripts and submition of compiled card data to TCG Arena (e.g. use of Github Workflows).
- [ ] Fix Z-Extra images from the recent sets that appear to have whitespaces above and below.
- [ ] Fix use of tokens and energy markers.
- [ ] Improve game file whenever there are new features and updates to TCG Arena.

## Acknowledgments
Special thanks to:
* Adam and the [Deckplanet](https://www.deckplanet.net) team for all the support and card data they provided.
* [TCG Arena](https://www.tcg-arena.fr) team for the amazing platform that helps ship card games to digital.
* All the testers that used their free time to point out errors, potential enhancements and future concerns. 
