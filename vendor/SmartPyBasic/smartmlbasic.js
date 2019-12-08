/* Copyright 2019 Smart Chain Arena LLC. */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);

// smartmljs.bc.js requires this to be succeed loading, of course,
// crypto-related functions won't work:
global.eztz = {
    prefix : { edsig : undefined, edsk : undefined,
               edsk2 : undefined, edpk : undefined }
}
smartml=require(__dirname + '/smartmljs.bc.js');

var mode          = "";
var compile       = undefined;
var outputDir     = "";
var targetStorage = "";
var targetCode    = "";
var targetTypes  = "";
var scenario      = undefined;

for (var i = 0; i < args.length; i++)
{
    switch(args[i]) {
    case "--compile":
        mode = "compile";
        break;
    case "--outputDir":
        mode = "outputDir";
        break;
    case "--targetCode":
        mode = "targetCode"
        break;
    case "--targetStorage":
        mode = "targetStorage"
        break;
    case "--targetTypes":
        mode = "targetTypes"
        break;
    case "--scenario":
        mode = "scenario"
        break;
    default:
        if (mode == "compile")
        {
            compile = args[i];
        }
        else if (mode == "outputDir")
        {
            outputDir = args[i];
        }
        else if (mode == "targetCode")
        {
            targetCode = args[i];
        }
        else if (mode == "targetStorage")
        {
            targetStorage = args[i];
        }
        else if (mode == "targetTypes")
        {
            targetTypes = args[i];
        }
        else if (mode == "scenario")
        {
            scenario = args[i];
        }
        else
        {
            throw "Bad command line. " + args[i];
        }
    }
}

function ppToFile(filename, target, value)
{
    if (target)
    {
        fs.writeFileSync(target, value);
    }
    else if (outputDir)
    {
        fs.writeFileSync(outputDir + "/" + filename, value);
    }
    else{
        console.log("==== " + filename + " ====");
        console.log(value);
    }
}


if (compile != undefined)
{
    const s_expr = fs.readFileSync(args[1], 'utf8');
    const contract = smartml.importContract(s_expr);
    // ppToFile("contractStorage.tz", targetStorage, smartml.compileContractStorage(contract));
    // ppToFile("contractTypes.tz", targetTypes, smartml.ppContractTypes(contract));
    const compiledContract = smartml.compileContract(contract);
    const basename = path.basename(args[1], path.extname(args[1]))
    // ppToFile(`${basename}.tz`, targetCode, smartml.compiledContract_to_michelson(compiledContract));
    // ppToFile(`${basename}.json`, targetCode, smartml.compiledContract_to_micheline(compiledContract));
    fs.writeFileSync(`${outputDir}/${basename}.tz`, smartml.compiledContract_to_michelson(compiledContract));
    fs.writeFileSync(`${outputDir}/${basename}.json`, smartml.compiledContract_to_micheline(compiledContract));
}


if (scenario != undefined)
{
    smartml.runScenario(scenario, outputDir)
}
