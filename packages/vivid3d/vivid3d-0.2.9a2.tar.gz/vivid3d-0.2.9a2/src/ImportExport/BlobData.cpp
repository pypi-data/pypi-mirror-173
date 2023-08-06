#include "BlobData.h"
#include "LogFile.h"

using namespace std;
using namespace vivid;

CBlobData CBlobData::FormatExportDataBlob(const aiExportDataBlob *apBlob) {
    auto blob = apBlob;

    std::vector<std::string> names;
    std::vector<char*> files;

    while (blob->data) {
        names.emplace_back(blob->name.C_Str());
        auto file = new char[blob->size];
        memcpy(file, (char*)(blob->data), blob->size);
        files.push_back(file);
        if (!blob->next) {
            break;
        }
        blob = blob->next;
    }
    return CBlobData(names.size(), names, files);
}
