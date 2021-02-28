# Sub Maps 
 
 <a href="https://raw.githubusercontent.com/paulowe/maps4resources/master/examples/Screen%20Shot%202021-01-11%20at%203.52.12%20AM.png" target="_blank"><img src="examples/Screen Shot 2021-01-11 at 3.52.12 AM.png" align="center" width="500" alt="OER Map"></a>

## About Sub Maps

This is a branch created from master. It is specifically for making enhancements to the architecture of the resource map - [https://aif-mvp.herokuapp.com] so that as an admin you can dynamically create sub-maps also termed as 'locales' and generate new subdomains for each one. At the moment this is the main feature we are actively working on to improve our current offering. All changes from this branch will eventually be merged back into master once we complete the feature.

Feel free to submit PRs and contirbute your changes.

### Submap (Locale)
A Locale is another map and a set of pins in that map. These pins are maintained by a University/Classroom that is using our project. 

Each locale will have a URL under aif-mvp.herokuapp.com/X where X is the name of the locale. 

For example, "aif-mvp.herokuapp.com/EECS3421" can be a locale in which a professor Manos Papagelis can collaborate with his/her students to create a set of pins used in their class. 

### Main map
To visualize how each university/class is using our map. We will also create a main map. This map is responsible for showing all locales and uses the subdomain name "all-maps" so its URL will be aif-mvp.herokuapp.com/all-maps. 

As an admin of the site, you can create or remove locales.

### Proposed improvements to current offering

-> Create a 'locale / submap' database table to store records of each submap

-> Create specific subdomain url links for each locale

-> Create one-to-many relationships between a locale and resources

-> Update each locale path to display its own set of resources (changes to how you query the database)

-> Ondelete -> we should cascade delete all pins related to the locale

-> Create new account type (manager) that has admin rights to manage their own locales, but not the entire map

## License
[MIT License](LICENSE.md)
