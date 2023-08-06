#ifndef VIVID_BLOBDATA_H
#define VIVID_BLOBDATA_H

#include "assimp/cexport.h"
#include <vector>
#include <string>

namespace vivid {
    struct CBlobData {
        const size_t mNumFiles;
        const std::vector<std::string> mNames;
        const std::vector<char*> mFiles;

        CBlobData() : mNumFiles(), mNames(), mFiles() {}
        CBlobData(const size_t aNumFiles, const std::vector<std::string>& arNames, const std::vector<char*>& apFiles)
            : mNumFiles(aNumFiles), mNames(arNames), mFiles(apFiles) { }

        ~CBlobData() = default;

        static CBlobData FormatExportDataBlob(const aiExportDataBlob* apBlob);
    };

}; // namespace vivid
#endif //VIVID_BLOBDATA_H
