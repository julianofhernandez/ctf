## Overview
We intend to model the structure of our metadata using the [W3C standards](https://www.w3.org/TR/tabular-data-primer/) but we are not able to completely follow these standards since CTF is different from CSV. Thus, in this writing we will examine how we will differ from W3C and what the advanctages and disadvantages are in the way that we proceed with our format.

## Example CSV
The following is a CSV file,`vgsales.csv` that we will use to illustrate the differences.

```CSV
Rank,Name,Platform,Year, Global_Sales
1,Wii Sports,Wii,2006,82.74
2,Super Mario Bros.,NES,1985,40.74
3,Mario Kart Wii,Wii,2008,35.82
4,Wii Sports Resort,Wii,2009,33
5,Pokemon Red/Pokemon Blue,GB,1996,31.37
```
## Example CTF
The CSV file would be repsented in CTF by a directory named `vgsales` and would contain files for each column like this.

`Rank.txt` contains 
```
1
2
3
4
5
```

`Name.txt` contains 
```
Wii Sports
Super Mario Bros.
Mario Kart Wii
Wii Sports Resort
Pokemon Red/Pokemon Blue
```
`Platform.txt` contains
```
Wii
NES
Wii
Wii
GB
```


`Year.txt` contains 
```
2006
1985
2008
2009
1996
```

`Global_Sales.txt` contains
```

82.74
40.24
35.82
33
31.37
```

## Example CSV metadata 
This is how its metadata would be written according to W3C standards 

```JSON
{
	"@context": "http://www.w3.org/ns/csvw",
	"url": "vgsales.csv",
	"tableSchema": {
		"columns": [{
			"titles": "Rank",
			"description": "The rank of different video games based on their global sales.", 
			"datatype": {
				"base": "integer",
				"minimum": "1"
				}
			}, {
			"titles": "Name",
			"description": "The name of the video game."
			}, {
			"titles": "Platform",
			"description": "The type of device or console the came is played on."
			}, {
			"titles": "Year",
			"description": "The year the game was released.",
			"datatype": {
				"base": "gYear",
				"minimum": "1958"
				}
			}, {
			"titles": "Global_Sales",
			"description": "The sales of the game in millions of units globally.",
			"datatype":{
				"base": "number",
				"minimum": "0"
				}
			}]
		}
}
```
As seen above, there is a url to specify `vgsales.csv` and then "tableSchema" that contains "columns" which have information on each of the columns. We are unable to represent a CSV file in this manner since instead of simply being one file with multiple columns, we have a directory with multiple files. It is beneficial to keep as close to W3C standards as possible since users are familiar with that format and likely a lot of thought went into developing those standards so we don't want to have to reinvent too much. 

First, we will show how we can handle the issue arising from CTF being a directory instead of a single file. 
Instead of having "URL" correspond to a CSV file we can have it correspond to the name of the CTF directory. We can call this "dir".
Further, we also need to recognize that "columns" will be files instead of CSV columns so we can change the name to "columnFiles" or something like that.
Lastly, we should include the name of the files associated with each columnFile and we can make a field called "url" to do this.

This is how a JSON implementation of the stated would look. 

```JSON
{
        "@context": "http://www.w3.org/ns/csvw",
        "dir": "vgsales",
        "tableSchema": {
            "columnFiles": [{
			    "url": "Rank.txt",
                "titles": "Rank",
                "description": "The rank of different video games based on their global sales.",
                "datatype": {
                        "base": "integer",
                        "minimum": "1"
                        }
                }, {
			    "url": "Name.txt",
                "titles": "Name",
                "description": "The name of the video game."
                }, {
                "titles": "Platform",
                "description": "The type of device or console the came is played on."
                }, {
			    "url": "Year.txt",
                "titles": "Year",
                "description": "The year the game was released.",
                "datatype": {
                        "base": "gYear",
                        "minimum": "1958"
                        }
                }, {
                "url": "Global_Sales.txt",
                "titles": "Global_Sales",
                "description": "The sales of the game in millions of units globally.",
                "datatype":{
                        "base": "number",
                        "minimum": "0"
                        }
                }]
            }
}
```
Since it is possible to have multiple files represent one column (if there is a lot of data we will break
up a single column into many seperate txt files) we will need to alter the "url" field to show all the 
files that correspond to an individual columnFile. We will store the files in an array strucutre since the 
indexing matters. Moreover, to keep the format simple for those who are not working with large amounts of 
data we can have a default since W3C uses defaulting (for instance, if nothing is put in "datatype" it will asume that 
the "datatype is a string). If an array is placed in the "url" field then we know that there are multiple text 
files corresponding to the single columnFile. Otherwise, we will keep it as the example above shows. 

This is an example with many text files per columnFile. I'm not sure how we want to name the files if there 
are many of them so I just put a "_int" to represent them. 

```JSON
{
        "@context": "http://www.w3.org/ns/csvw",
        "dir": "vgsales.csv",
        "tableSchema": {
                "columnFiles": [{
                        "url": ["Rank_1.txt", "Rank_2.txt", "Rank_3.txt"],
                        "titles": "Rank",
                        "description": "The rank of different video games based on their global sales.",
                        "datatype": {
                                "base": "integer",
                                "minimum": "1"
                                }
                        }, {
                        "url": ["Name_1.txt", "Name_2.txt", "Name_3.txt"], 
                        "titles": "Name",
                        "description": "The name of the video game."
                        }, {
                        "titles": "Platform",
                        "description": "The type of device or console the came is played on."
                        }, {
                        "url": ["Year_1.txt","Year_2.txt","Year_3.txt"],
                        "titles": "Year",
                        "description": "The year the game was released.",
                        "datatype": {
                                "base": "gYear",
                                "minimum": "1958"
                                }
                        }, {
                        "url": ["Global_Sales_1.txt","Global_Sales_2.txt","Global_Sales_3.txt"],
                        "titles": "Global_Sales",
                        "description": "The sales of the game in millions of units globally.",
                        "datatype":{
                                "base": "number",
                                "minimum": "0"
                                }
                        }]
                }
}
```

The main advantage of this is the formatting is rather simple and feels a lot like how 
one would work with a single CSV file. The disadvantage, that I personally see since I may be missing
some, is that it differs in the way that W3C recommends one follow if they have multiple CSV files.

Here is an example from their website (example 35) of how they handle multiple CSV files. 

```JSON
{
  "@context": "http://www.w3.org/ns/csvw",
  "tables": [{
    "url": "countries.csv",
    "tableSchema": {
      "columns": [{
        "titles": "country"
      },{
        "name": "country_group",
        "titles": "country group"
      },{
        "titles": "name (en)"
      },{
        "titles": "name (fr)"
      },{
        "titles": "name (de)"
      },{
        "titles": "latitude"
      },{
        "titles": "longitude"
      }]
    }
  }, {
    "url": "country-groups.csv",
    "tableSchema": {
      "columns": [{
        "name": "group",
        "titles": "group"
      }]
    }
  }]
}
```

Thus we could try and mimic this format and simply replace the CSV files with txt files. This is what it would look like.

```JSON
{
  "@context": "http://www.w3.org/ns/csvw",
  "title": "vgsales",
  "description": "Data on the highest selling video games around the world.",
  "creator": "Gregory Smith",
  "tables": [{
    "url": "Rank.txt",
    "tableSchema": {
      "columns": [{
        "name": "Rank",
        "titles": "Rank",
        "description": "The rank of different video games based on their global sales.",
        "datatype": {
          "base": "integer",
          "minimum": "1"
        }
      }],
  }
  }, {
    "url": "Name.txt",
    "tableSchema": {
      "columns": [{
        "titles": "Name",
        "description": "The name of the video game."
      }]
  }
  }, {
    "url": "Platform.txt",
    "tableSchema": {
      "columns": [{
        "titles": "Platform",
        "description": "The type of device or console the game is played on."
      }]
  }
  }]
}
```

However, this way is much more repetitive and cluttered than the previously shown format.
As one can observe, there are each url has its own "tableSchema" and "columns" but in the previously
suggested format there is only one "tableSchema" and "columns" is instead denoted by a single structure 
called "columnFiles" which encompasses all the files of the CTF directory. 
It would get even more cluttered if each columnFile had several corresponding text files. For instance,
if the columnFile Platform was so large that it had two text files, "Platform_1.txt" and "Platform_2.txt"
associated with it, then there would be nearly identical tableSchemas  for two different urls.

## Where the metadata file will be stored
The metadata file will be stored in the CTF directory and will have share the directory's name but will have -metadata.json appended to it. For instance, a CTF directory named `vgsales` would contain a metadata file named `vgsales-metadata.json.

## JSON-LD contexts
Sources [A JSON-based Serialization for Linked Data](https://www.w3.org/TR/json-ld11/#introduction) and (https://www.w3.org/TR/tabular-data-primer/)
### What exactly is a context?
* When two people communicate with one another, the conversation takes place in a shared environment, typically called "the context of the conversation". This shared context allows the individuals to use shortcut terms, like the first name of a mutual friend, to communicate more quickly but without losing accuracy. A context in JSON-LD works in the same way. It allows two applications to use shortcut terms to communicate with one another more efficiently, but without losing accuracy.
* A context is used to map term, case sensitive short-hand string that cannot be the same as any JSON-LD keyword, to [IRIs](https://tools.ietf.org/html/rfc3987#section-2). 
* Information in the referenced context allows developers to re-use each other's data without having to agree to how their data will interoperate on a site-by-site basis. 
* Metadata files must always include the @context property with a value "http://www.w3.org/ns/csvw": this enables implementations to tell that these are CSV metadata files. The url property points to the CSV file that the metadata file describes.

### How will differ from the CSVW context
First note that we will try to extend as much from CSVW as we can.
* We will not have `columns` since these are used to specify the particular columns that a CSV file has and instead we will have an anologous idea called `columnFiles` which has already been explained.
* We will not use `url` to link to a CSV file and instead we will use `url` to link to a text file or an array of text files that correspond to one specific columnFile. 
* We will create a new property definition called `dir` which will serve as the structure for CTF file.   

## Clark's comments

`dir` as the directory name could be a URL more generally, and then we can understand the URL for each column to be relative to the top level URL.
It might make more sense to put the columns in a directory underneath the metadata.
We could also just say `"url": "."` to denote the local directory where the metadata file lives.
We also need the metadata to give the name of the table.

Here's another way to structure it:

```JSON
{
        "@context": "http://www.w3.org/ns/csvw",
        "url": ".",
        "name": "vgsales",
        "rowCount": 15000,
        "tableSchema": {
            "columnFiles": [{
			    "url": "Rank.txt",
                "titles": "Rank",
                "description": "The rank of different video games based on their global sales.",
                "datatype": "integer"
                }]
            }
}
```

Programming languages won't need a `"name"` for the table, but a database crawler will.

`rowCount` is derived from `headerRowCount` in the official spec.
It says how many rows are in the data.

