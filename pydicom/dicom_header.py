typedef struct _DcmFilehandle DcmFilehandle;
typedef struct _DcmElement DcmElement;
typedef struct _DcmDataSet DcmDataSet;
typedef struct _DcmSequence DcmSequence;
typedef struct _DcmFrame DcmFrame;

enum _DcmErrorCode {
    DCM_ERROR_CODE_NOMEM = 1,
    DCM_ERROR_CODE_INVALID = 2,
    DCM_ERROR_CODE_PARSE = 3,
    DCM_ERROR_CODE_IO = 4,
};

typedef enum _DcmErrorCode DcmErrorCode;

typedef enum _DcmVR {
    DCM_VR_ERROR = -1,

    DCM_VR_AE = 0,
    DCM_VR_AS,
    DCM_VR_AT,
    DCM_VR_CS,
    DCM_VR_DA,
    DCM_VR_DS,
    DCM_VR_DT,
    DCM_VR_FL,
    DCM_VR_FD,
    DCM_VR_IS,
    DCM_VR_LO,
    DCM_VR_LT,
    DCM_VR_OB,
    DCM_VR_OD,
    DCM_VR_OF,
    DCM_VR_OW,
    DCM_VR_PN,
    DCM_VR_SH,
    DCM_VR_SL,
    DCM_VR_SQ,
    DCM_VR_SS,
    DCM_VR_ST,
    DCM_VR_TM,
    DCM_VR_UI,
    DCM_VR_UL,
    DCM_VR_UN,
    DCM_VR_US,
    DCM_VR_UT,
    DCM_VR_UR,
    DCM_VR_UC,
    DCM_VR_OL,
    DCM_VR_OV,
    DCM_VR_SV,
    DCM_VR_UV,

} DcmVR;

const char *dcm_error_code_str(int code);
const char *dcm_error_code_name(int code);

typedef struct _DcmError DcmError;

const char *dcm_error_get_summary(DcmError *error);
const char *dcm_error_get_message(DcmError *error);
int dcm_error_get_code(DcmError *error);

void dcm_error_log(DcmError *error);

enum _DcmLogLevel {
    DCM_LOG_CRITICAL = 50,
    DCM_LOG_ERROR = 40,
    DCM_LOG_WARNING = 30,
    DCM_LOG_INFO = 20,
    DCM_LOG_DEBUG = 10,
    DCM_LOG_NOTSET = 0,
};


int dcm_dict_vr_from_str(const char *vr);
const char *dcm_dict_str_from_vr(int vr);

const char *dcm_dict_keyword_from_tag(int tag);
int dcm_dict_tag_from_keyword(const char *keyword);

int dcm_vr_from_tag(int tag);

bool dcm_is_public_tag(int tag);

bool dcm_is_private_tag(uint32_t tag);

/**
 * Determine whether a Tag is valid.
 *
 * :param tag: Attribute Tag
 *
 * :return: Yes/no answer
 */
DCM_EXTERN
bool dcm_is_valid_tag(uint32_t tag);

/**
 * Determine whether a Value Representation is valid.
 *
 * :param vr: Attribute Value Representation
 *
 * :return: Yes/no answer
 */
DCM_EXTERN
bool dcm_is_valid_vr(const char *vr);

/**
 * Determine whether a Value Representation is valid.
 *
 * :param vr: Attribute Value Representation
 *
 * :return: Yes/no answer
 */
DCM_EXTERN
bool dcm_is_valid_vr_for_tag(DcmVR vr, uint32_t tag);

/**
 * Determine whether a Transfer Syntax is encapsulated.
 *
 * :param transfer_syntax_uid: Transfer Syntax UID
 *
 * :return: Yes/no answer
 */
DCM_EXTERN
bool dcm_is_encapsulated_transfer_syntax(const char *transfer_syntax_uid);


/**
 * Data Element
 */

/**
 * Create a Data Element for a tag.
 *
 * After creating a Data Element, you must
 * attach an appropriate value using one of the setting functions.
 * See for example :c:func:`dcm_element_set_value_string`.
 *
 * :param error: Pointer to error object
 * :param tag: Tag
 * :param vr: The Value Representation for this Data Element
 *
 * :return: Pointer to Data Element
 */
DCM_EXTERN
DcmElement *dcm_element_create(DcmError **error, uint32_t tag, DcmVR vr);

/**
 * Get group number (first part of Tag) of a Data Element.
 *
 * :param element: Pointer to Data Element
 *
 * :return: Tag group number
 */
DCM_EXTERN
uint16_t dcm_element_get_group_number(const DcmElement *element);

/**
 * Get Element Number (second part of Tag) of a Data Element.
 *
 * :param element: Pointer to Data Element
 *
 * :return: Tag Element Number
 */
DCM_EXTERN
uint16_t dcm_element_get_element_number(const DcmElement *element);

/**
 * Get Tag of a Data Element.
 *
 * :param element: Pointer to Data Element
 *
 * :return: Tag
 */
DCM_EXTERN
uint32_t dcm_element_get_tag(const DcmElement *element);

/**
 * Get the Value Representation of a Data Element.
 *
 * :param element: Pointer to Data Element
 *
 * :return: Value Representation
 */
DCM_EXTERN
DcmVR dcm_element_get_vr(const DcmElement *element);

/**
 * Get length of the entire value of a Data Element.
 *
 * :param element: Pointer to Data Element
 *
 * :return: Length of value of Data Element
 */
DCM_EXTERN
uint32_t dcm_element_get_length(const DcmElement *element);

/**
 * Get Value Multiplicity of a Data Element.
 *
 * :param element: Pointer to Data Element
 *
 * :return: Value Multiplicity
 */
DCM_EXTERN
uint32_t dcm_element_get_vm(const DcmElement *element);

/**
 * Determine whether a Data Element has a Value Multiplicity greater than one.
 *
 * :param element: Pointer to Data Element
 *
 * :return: Yes/no answer
 */
DCM_EXTERN
bool dcm_element_is_multivalued(const DcmElement *element);

/**
 * Clone (i.e., create a deep copy of) a Data Element.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 *
 * :return: Pointer to clone of Data Element
 */
DCM_EXTERN
DcmElement *dcm_element_clone(DcmError **error, const DcmElement *element);

/**
 * Get a string from a string-valued Data Element.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param index: Zero-based index of value within the Data Element
 * :param value: Pointer to return location for value 
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_element_get_value_string(DcmError **error,
                                  const DcmElement *element,
                                  uint32_t index,
                                  const char **value);

/**
 * Set the value of a Data Element to a character string.
 *
 * The Data Element must have a Tag that allows for a
 * character string Value Representation.
 * If that is not the case, the function will fail.
 *
 * On success, if `steal` is true, ownership of `value` passes to
 * `element`, i.e. it will be freed when `element` is destroyed. If `steal` is
 * false, then a copy is made of `value` and ownership is not transferred.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param value: String value
 * :param steal: if true, ownership of value passes to element
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_element_set_value_string(DcmError **error,
                                  DcmElement *element,
                                  char *value,
                                  bool steal);

/**
* Set the value of a Data Element to an array of character strings.
 *
 * The Data Element must have a Tag that allows for a
 * character string Value Representation and for a
 * Value Multiplicity greater than one.
 * If that is not the case, the function will fail.
 *
 * On success, if `steal` is true, ownership of `value` passes to
 * `element`, i.e. it will be freed when `element` is destroyed. If `steal` is
 * false, then a copy is made of `value` and ownership is not transferred.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param values: Pointer to memory location where values are written to
 * :param vm: Number of values
 * :param steal: if true, ownership of values passes to element
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_element_set_value_string_multi(DcmError **error,
                                        DcmElement *element,
                                        char **values,
                                        uint32_t vm,
                                        bool steal);

/**
 * Get an integer from a 16, 32 or 64-bit integer-valued Data Element.
 *
 * The integer held in the Element will be cast to int64_t for return.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param index: Zero-based index of value within the Data Element
 * :param value: Pointer to return location for value 
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_element_get_value_integer(DcmError **error,
                                   const DcmElement *element,
                                   uint32_t index,
                                   int64_t *value);

/**
 * Set the value of a Data Element to an integer.
 * 
 * The Data Element must have a Tag that allows for a
 * integer Value Representation.
 * If that is not the case, the function will fail.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param value: Integer value
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_element_set_value_integer(DcmError **error,
                                   DcmElement *element,
                                   int64_t value);

/**
 * Set the value of a Data Element to a number.
 * 
 * The Data Element must have a Tag that allows for a
 * numeric Value Representation.
 * If that is not the case, the function will fail.
 *
 * Although the value passed is `void*`, it should
 * be a pointer to an array of 16- to 64-bit numeric values of the
 * appropriate type for the Data Element Value Representation.
 *
 * On success, if `steal` is true, ownership of `values` passes to
 * `element`, i.e. it will be freed when `element` is destroyed. If `steal` is
 * false, then a copy is made of `values` and ownership is not transferred.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param values: Array of values
 * :param vm: Number of values
 * :param steal: if true, ownership of values passes to element
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_element_set_value_numeric_multi(DcmError **error,
                                         DcmElement *element,
                                         void *values,
                                         uint32_t vm,
                                         bool steal);

/**
 * Get a floating-point value from a Data Element.
 *
 * The Data Element Value Reepresentation may be either single- or 
 * double-precision floating point.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param index: Zero-based index of value within the Data Element
 * :param value: Pointer to return location for value 
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_element_get_value_floatingpoint(DcmError **error,
                                         const DcmElement *element,
                                         uint32_t index,
                                         double *value);

/**
 * Set the value of a Data Element to a floating-point.
 * 
 * The Data Element must have a Tag that allows for a
 * floating-point Value Representation.
 * If that is not the case, the function will fail.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param value: Floating point value
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_element_set_value_floatingpoint(DcmError **error,
                                         DcmElement *element,
                                         double value);

/**
 * Get a binary value from a Data Element.
 *
 * Use :c:func:`dcm_element_length` to get the length of the binary value.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param value: Pointer to return location for value 
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_element_get_value_binary(DcmError **error,
                                  const DcmElement *element,
                                  const char **value);

/**
 * Set the value of a Data Element to binary data.
 * 
 * The Data Element must have a Tag that allows for a
 * binary Value Representation.
 * If that is not the case, the function will fail.
 *
 * On success, if `steal` is true, ownership of `value` passes to
 * `element`, i.e. it will be freed when `element` is destroyed. If `steal` is
 * false, then a copy is made of `value` and ownership is not transferred.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param value: Pointer to binary value
 * :param length: Length in bytes of the binary value
 * :param steal: if true, ownership of the value passes to element
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_element_set_value_binary(DcmError **error,
                                  DcmElement *element,
                                  char *value,
                                  uint32_t length,
                                  bool steal);

/* Set a value for an Element from a generic byte buffer. The byte buffer must 
 * have been correctly formatted for the VR of this Element.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param value: Pointer to value
 * :param length: Length in bytes of the value
 * :param steal: if true, ownership of the value passes to element
 *
 * :return: true on success
 */
bool dcm_element_set_value(DcmError **error,                                   
                           DcmElement *element,
                           char *value,
                           uint32_t length,
                           bool steal);

/**
 * Get a sequence value from a Data Element.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param value: Pointer to return location for value 
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_element_get_value_sequence(DcmError **error,
                                    const DcmElement *element,
                                    DcmSequence **value);


/**
 * Set the value of a Data Element to a Sequence.
 * 
 * The Data Element must have a Tag that allows for
 * Value Representation ``"SQ"``.
 * If that is not the case, the function will fail.
 *
 * The Data Element takes ownership of the value pointer on success.
 *
 * :param error: Pointer to error object
 * :param element: Pointer to Data Element
 * :param value: Pointer to Sequence
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_element_set_value_sequence(DcmError **error,
                                    DcmElement *element,
                                    DcmSequence *value);

/**
 * Print a Data Element.
 *
 * :param element: Pointer to Data Element
 * :param indentation: Number of white spaces before text
 */
DCM_EXTERN
void dcm_element_print(const DcmElement *element, int indentation);

/**
 * Destroy a Data Element.
 *
 * :param element: Pointer to Data Element
 */
DCM_EXTERN
void dcm_element_destroy(DcmElement *element);


/**
 * Data Set
 */

/**
 * Create an empty Data Set.
 *
 * :param error: Pointer to error object
 */
DCM_EXTERN
DcmDataSet *dcm_dataset_create(DcmError **error);

/**
 * Clone (i.e., create a deep copy of) a Data Set.
 *
 * :param error: Pointer to error object
 * :param dataset: Pointer to Data Set
 *
 * :return: Pointer to clone of Data Set
 */
DCM_EXTERN
DcmDataSet *dcm_dataset_clone(DcmError **error, const DcmDataSet *dataset);

/**
 * Insert a Data Element into a Data Set.
 *
 * :param error: Pointer to error object
 * :param dataset: Pointer to Data Set
 * :param element: Pointer to Data Element
 *
 * The object takes over ownership of the memory referenced by `element`
 * and frees it when the object is destroyed or if the insert operation fails.
 *
 * :return: Whether insert operation was successful
 */
DCM_EXTERN
bool dcm_dataset_insert(DcmError **error,
                        DcmDataSet *dataset, DcmElement *element);

/**
 * Remove a Data Element from a Data Set.
 *
 * :param error: Pointer to error object
 * :param dataset: Pointer to Data Set
 * :param tag: Attribute Tag of a Data Element
 *
 * :return: Whether remove operation was successful
 */
DCM_EXTERN
bool dcm_dataset_remove(DcmError **error, DcmDataSet *dataset, uint32_t tag);

/**
 * Get a Data Element from a Data Set.
 *
 * :param error: Pointer to error object
 * :param dataset: Pointer to Data Set
 * :param tag: Attribute Tag of a Data Element
 *
 * :return: Pointer to Data Element
 */
DCM_EXTERN
DcmElement *dcm_dataset_get(DcmError **error,
                            const DcmDataSet *dataset, uint32_t tag);

/**
 * Get a clone (deep copy) of a Data Element from a Data Set.
 *
 * :param error: Pointer to error object
 * :param dataset: Pointer to Data Set
 * :param tag: Attribute Tag of a Data Element
 *
 * :return: Pointer to clone of Data Element
 */
DCM_EXTERN
DcmElement *dcm_dataset_get_clone(DcmError **error,
                                  const DcmDataSet *dataset, uint32_t tag);

/**
 * Iterate over Data Elements in a Data Set.
 *
 * Does not sort Data Elements, but iterates over them in the order in which
 * they were originally inserted into the Data Set.
 *
 * :param dataset: Pointer to Data Set
 * :param fn: Pointer to function that should be called for each Data Element
 */
DCM_EXTERN
void dcm_dataset_foreach(const DcmDataSet *dataset,
                         void (*fn)(const DcmElement *element));

/**
 * Fetch a Data Element from a Data Set, or NULL if not present.
 *
 * :param dataset: Pointer to Data Set
 * :param tag: Attribute Tag of a Data Element
 *
 * :return: Data Element, or NULL if not present
 */
DCM_EXTERN
DcmElement *dcm_dataset_contains(const DcmDataSet *dataset, uint32_t tag);

/**
 * Count the number of Data Elements in a Data Set.
 *
 * :param dataset: Pointer to Data Set
 *
 * :return: Number of Data Elements
 */
DCM_EXTERN
uint32_t dcm_dataset_count(const DcmDataSet *dataset);

/**
 * Obtain a copy of the Tag of each Data Element in a Data Set.
 *
 * The tags will be sorted in ascending order.
 *
 * :param dataset: Pointer to Data Set
 * :param tags: Pointer to memory location to of the array into which to copy
 *              tags. Number of items in the array must match the number of
 *              Data Elements in the Data Set as determined by
 *              :c:func:`dcm_dataset_count`.
 * :param n: Number of items in the array.
 *
 * Ownership of the memory allocated for `tags` remains with the caller.
 * Specifically, the function does not free the memory allocated for `tags` if
 * the copy operation fails.
 */
DCM_EXTERN
void dcm_dataset_copy_tags(const DcmDataSet *dataset, uint32_t *tags,
                           uint32_t n);

/**
 * Lock a Data Set to prevent modification.
 *
 * :param dataset: Pointer to Data Set
 */
DCM_EXTERN
void dcm_dataset_lock(DcmDataSet *dataset);

/**
 * Check whether a Data Set is locked.
 *
 * :param dataset: Pointer to Data Set
 *
 * :return: Yes/no answer
 */
DCM_EXTERN
bool dcm_dataset_is_locked(const DcmDataSet *dataset);

/**
 * Print a Data Set.
 *
 * :param error: Pointer to error object
 * :param dataset: Pointer to Data Set
 * :param indentation: Number of white spaces before text
 */
DCM_EXTERN
void dcm_dataset_print(const DcmDataSet *dataset, int indentation);

/**
 * Destroy a Data Set.
 *
 * :param dataset: Pointer to Data Set
 */
DCM_EXTERN
void dcm_dataset_destroy(DcmDataSet *dataset);


/**
 * Sequence
 */

/**
 * Create a Sequence, i.e., a collection of Data Set items that represent the
 * value of a Data Element with Value Representation SQ (Sequence).
 *
 * Note that created object represents the value of a Data Element rather
 * than a Data Element itself.
 *
 * :param error: Pointer to error object
 * :return: Pointer to Sequence
 */
DCM_EXTERN
DcmSequence *dcm_sequence_create(DcmError **error);

/**
 * Append a Data Set item to a Sequence.
 *
 * :param error: Pointer to error object
 * :param seq: Pointer to Sequence
 * :param item: Data Set item
 *
 * The object takes over ownership of the memory referenced by `item`
 * and frees it when the object is destroyed or if the append operation fails.
 *
 * :return: Whether append operation was successful
 */
DCM_EXTERN
bool dcm_sequence_append(DcmError **error,
                         DcmSequence *seq, DcmDataSet *item);

/**
 * Get a Data Set item from a Sequence.
 *
 * :param error: Pointer to error object
 * :param seq: Pointer to Sequence
 * :param index: Zero-based index of the Data Set item in the Sequence
 *
 * :return: Pointer to Data Set item
 */
DCM_EXTERN
DcmDataSet *dcm_sequence_get(DcmError **error,
                             const DcmSequence *seq, uint32_t index);

/**
 * Iterate over Data Set items in a Sequence.
 *
 * :param seq: Pointer to Sequence
 * :param fn: Pointer to function that should be called for each Data Set item
 */
DCM_EXTERN
void dcm_sequence_foreach(const DcmSequence *seq,
                          void (*fn)(const DcmDataSet *item));

/**
 * Remove a Data Set item from a Sequence.
 *
 * :param error: Pointer to error object
 * :param seq: Pointer to Sequence
 * :param index: Zero-based index of the Data Set item in the Sequence
 *
 * :return: Whether remove operation was successful
 */
DCM_EXTERN
bool dcm_sequence_remove(DcmError **error, DcmSequence *seq, uint32_t index);

/**
 * Count the number of Data Set items in a Sequence.
 *
 * :param seq: Pointer to Sequence
 *
 * :return: number of Data Set items
 */
DCM_EXTERN
uint32_t dcm_sequence_count(const DcmSequence *seq);

/**
 * Lock a Sequence to prevent modification.
 *
 * :param seq: Pointer to Sequence
 */
DCM_EXTERN
void dcm_sequence_lock(DcmSequence *seq);

/**
 * Check whether a Sequence is locked.
 *
 * :param seq: Pointer to Sequence
 *
 * :return: Yes/no answer
 */
DCM_EXTERN
bool dcm_sequence_is_locked(const DcmSequence *seq);

/**
 * Destroy a Sequence.
 *
 * :param seq: Pointer to Sequence
 */
DCM_EXTERN
void dcm_sequence_destroy(DcmSequence *seq);


/**
 * Frame
 *
 * Encoded pixels of an individual pixel matrix and associated
 * descriptive metadata.
 */

/**
 * Create a Frame.
 *
 * :param error: Pointer to error object
 * :param index: Index of the Frame within the Pixel Data Element
 * :param data: Pixel data of the Frame
 * :param length: Size of the Frame (number of bytes)
 * :param rows: Number of rows in pixel matrix
 * :param columns: Number of columns in pixel matrix
 * :param samples_per_pixel: Number of samples per pixel
 * :param bits_allocated: Number of bits allocated per pixel
 * :param bits_stored: Number of bits stored per pixel
 * :param pixel_representation: Representation of pixels
 *                              (unsigned integers or 2's complement)
 * :param planar_configuration: Configuration of samples
 *                              (color-by-plane or color-by-pixel)
 * :param photometric_interpretation: Interpretation of pixels
 *                                    (monochrome, RGB, etc.)
 * :param transfer_syntax_uid: UID of transfer syntax in which data is encoded
 *
 * The object takes over ownership of the memory referenced by `data`,
 * `photometric_interpretation`, and `transfer_syntax_uid`
 * and frees it when the object is destroyed or if the creation fails.
 *
 * :return: Frame Item
 */
DCM_EXTERN
DcmFrame *dcm_frame_create(DcmError **error,
                           uint32_t number,
                           const char *data,
                           uint32_t length,
                           uint16_t rows,
                           uint16_t columns,
                           uint16_t samples_per_pixel,
                           uint16_t bits_allocated,
                           uint16_t bits_stored,
                           uint16_t pixel_representation,
                           uint16_t planar_configuration,
                           const char *photometric_interpretation,
                           const char *transfer_syntax_uid);

/**
 * Get number of a Frame Item within the Pixel Data Element.
 *
 * :param frame: Frame
 *
 * :return: number (one-based index)
 */
DCM_EXTERN
uint32_t dcm_frame_get_number(const DcmFrame *frame);

/**
 * Get length of a Frame Item.
 *
 * :param frame: Frame
 *
 * :return: number of bytes
 */
DCM_EXTERN
uint32_t dcm_frame_get_length(const DcmFrame *frame);

/**
 * Get Rows of a Frame.
 *
 * :param frame: Frame
 *
 * :return: number of rows in pixel matrix
 */
DCM_EXTERN
uint16_t dcm_frame_get_rows(const DcmFrame *frame);

/**
 * Get Columns of a Frame.
 *
 * :param frame: Frame
 *
 * :return: number of columns in pixel matrix
 */
DCM_EXTERN
uint16_t dcm_frame_get_columns(const DcmFrame *frame);

/**
 * Get Samples per Pixel of a Frame.
 *
 * :param frame: Frame
 *
 * :return: number of samples (color channels) per pixel
 */
DCM_EXTERN
uint16_t dcm_frame_get_samples_per_pixel(const DcmFrame *frame);

/**
 * Get Bits Allocated of a Frame.
 *
 * :param frame: Frame
 *
 * :return: number of bits allocated per pixel
 */
DCM_EXTERN
uint16_t dcm_frame_get_bits_allocated(const DcmFrame *frame);

/**
 * Get Bits Stored of a Frame.
 *
 * :param frame: Frame
 *
 * :return: number of bits stored per pixel
 */
DCM_EXTERN
uint16_t dcm_frame_get_bits_stored(const DcmFrame *frame);

/**
 * Get High Bit of a Frame.
 *
 * :param frame: Frame
 *
 * :return: most significant bit of pixels
 */
DCM_EXTERN
uint16_t dcm_frame_get_high_bit(const DcmFrame *frame);

/**
 * Get Pixel Representation of a Frame.
 *
 * :param frame: Frame
 *
 * :return: representation of pixels (unsigned integers or 2's complement)
 */
DCM_EXTERN
uint16_t dcm_frame_get_pixel_representation(const DcmFrame *frame);

/**
 * Get Planar Configuration of a Frame.
 *
 * :param frame: Frame
 *
 * :return: configuration of samples (color-by-plane or color-by-pixel)
 */
DCM_EXTERN
uint16_t dcm_frame_get_planar_configuration(const DcmFrame *frame);

/**
 * Get Photometric Interpretation of a Frame.
 *
 * :param frame: Frame
 *
 * :return: interpretation of pixels (monochrome, RGB, etc.)
 */
DCM_EXTERN
const char *dcm_frame_get_photometric_interpretation(const DcmFrame *frame);

/**
 * Get Transfer Syntax UID for a Frame.
 *
 * :param frame: Frame
 *
 * :return: UID of the transfer syntax in which frame is encoded
 */
DCM_EXTERN
const char *dcm_frame_get_transfer_syntax_uid(const DcmFrame *frame);

/**
 * Get pixel data of a Frame.
 *
 * :param frame: Frame
 *
 * :return: pixel data
 */
DCM_EXTERN
const char *dcm_frame_get_value(const DcmFrame *frame);

/**
 * Destroy a Frame.
 *
 * :param frame: Frame
 */
DCM_EXTERN
void dcm_frame_destroy(DcmFrame *frame);


/**
 * Part 10 File
 */

typedef struct _DcmIOMethods DcmIOMethods;

/**
 * Something we can read from.
 */
typedef struct _DcmIO {
        const DcmIOMethods *methods;
        // more private fields follow
} DcmIO;

/**
 * A set of IO methods, see dcm_io_create().
 */
typedef struct _DcmIOMethods {
    /** Open an IO object */
    DcmIO *(*open)(DcmError **error, void *client);

    /** Close an IO object */
    void (*close)(DcmIO *io);

    /** Read from an IO object, semantics as POSIX read() */
    int64_t (*read)(DcmError **error, 
                    DcmIO *io, 
                    char *buffer, 
                    int64_t length);

    /** Seek an IO object, semantics as POSIX seek() */
    int64_t (*seek)(DcmError **error, 
                    DcmIO *io, 
                    int64_t offset, 
                    int whence);
} DcmIOMethods;

/**
 * Create an IO object using a set of IO methods.
 *
 * :param error: Error structure pointer
 * :param io: Set of read methods
 * :param client: Client data for read methods
 *
 * :return: IO object
 */
DCM_EXTERN
DcmIO *dcm_io_create(DcmError **error,
                     const DcmIOMethods *methods,
                     void *client);

/**
 * Open a file on disk for IO.
 *
 * :param error: Error structure pointer
 * :param filename: Path to the file on disk
 *
 * :return: IO object
 */
DCM_EXTERN
DcmIO *dcm_io_create_from_file(DcmError **error,
                               const char *filename);

/**
 * Open an area of memory for IO.
 *
 * :param error: Error structure pointer
 * :param buffer: Pointer to memory area
 * :param length: Length of memory area in bytes
 *
 * :return: IO object
 */
DCM_EXTERN
DcmIO *dcm_io_create_from_memory(DcmError **error,
                                 const char *buffer,
                                 int64_t length);

/**
 * Close an IO object.
 *
 * :param io: Pointer to IO object
 */
DCM_EXTERN
void dcm_io_close(DcmIO *io);

/**
 * Read from an IO object.
 *
 * Read up to length bytes from the IO object. Returns the number of bytes
 * read, or -1 for an error. A return of 0 indicates end of file.
 *
 * :param error: Pointer to error object
 * :param io: Pointer to IO object
 * :param buffer: Memory area to read to
 * :param length: Size of memory area
 *
 * :return: Number of bytes read
 */
DCM_EXTERN
int64_t dcm_io_read(DcmError **error,
                    DcmIO *io,
                    char *buffer,
                    int64_t length);

/**
 * Seek an IO object.
 *
 * Set whence to SEEK_CUR to seek relative to the current file position,
 * SEEK_END to seek relative to the end of the file, or SEEK_SET to seek
 * relative to the start. 
 *
 * Returns the new absolute read position, or -1 for IO error.
 *
 * :param error: Error structure pointer
 * :param io: Pointer to IO object
 * :param offset: Seek offset
 * :param whence: Seek mode
 *
 * :return: New read position
 */
DCM_EXTERN
int64_t dcm_io_seek(DcmError **error, 
                    DcmIO *io, 
                    int64_t offset, 
                    int whence);

/**
 * Create a representatiopn of a DICOM File using an IO object.
 *
 * The File object tracks information like the transfer syntax and the byte
 * ordering.
 *
 * :param error: Error structure pointer
 * :param io: IO object to read from
 *
 * :return: filehandle
 */
DCM_EXTERN
DcmFilehandle *dcm_filehandle_create(DcmError **error, DcmIO *io);

/**
 * Open a file on disk as a DcmFilehandle.
 *
 * :param error: Error structure pointer
 * :param filepath: Path to the file on disk
 *
 * :return: filehandle
 */
DCM_EXTERN
DcmFilehandle *dcm_filehandle_create_from_file(DcmError **error,
                                               const char *filepath);


/**
 * Open an area of memory as a DcmFilehandle.
 *
 * :param error: Error structure pointer
 * :param buffer: Pointer to memory area
 * :param length: Length of memory area in bytes
 *
 * :return: filehandle
 */
DCM_EXTERN
DcmFilehandle *dcm_filehandle_create_from_memory(DcmError **error,
                                                 const char *buffer, 
						 int64_t length);

/**
 * Destroy a Filehandle.
 *
 * :param filehandle: File
 */
DCM_EXTERN
void dcm_filehandle_destroy(DcmFilehandle *filehandle);

/**
 * Read File Meta Information from a File.
 *
 * Keeps track of the offset of the Data Set relative to the beginning of the
 * filehandle to speed up subsequent access, and determines the Transfer
 * Syntax in which the contained Data Set is encoded.
 *
 * :param error: Pointer to error object
 * :param filehandle: Pointer to file handle
 *
 * :return: File Meta Information
 */
DCM_EXTERN
DcmDataSet *dcm_filehandle_read_file_meta(DcmError **error,
                                          DcmFilehandle *filehandle);

/**
 * Read metadata from a File.
 *
 * Keeps track of the offset of the Pixel Data Element relative to the
 * beginning of the filehandle to speed up subsequent access to individual
 * Frame items.
 *
 * :param error: Pointer to error object
 * :param filehandle: File
 *
 * :return: metadata
 */
DCM_EXTERN
DcmDataSet *dcm_filehandle_read_metadata(DcmError **error,
                                         DcmFilehandle *filehandle);

/**
 * Read everything necessary to fetch frames from the file.
 *
 * Scans the PixelData sequence and loads the
 * PerFrameFunctionalGroupSequence, if present.
 *
 * :param error: Pointer to error object
 * :param filehandle: File
 *
 * :return: true on success
 */
DCM_EXTERN
bool dcm_filehandle_read_pixeldata(DcmError **error,
                                   DcmFilehandle *filehandle);

/**
 * Read the frame at a position in a File.
 *
 * Read a tile from a File at a specified (column, row), numbered from zero.
 * This takes account of any frame positioning given in 
 * PerFrameFunctionalGroupSequence, if necessary.
 *
 * :param error: Pointer to error object
 * :param filehandle: File
 * :param column: Column number, from 0
 * :param row: Row number, from 0
 *
 * :return: Frame
 */
DCM_EXTERN
DcmFrame *dcm_filehandle_read_frame_position(DcmError **error,
                                             DcmFilehandle *filehandle,
                                             uint32_t column,
                                             uint32_t row);

/**
 * Read an individual Frame from a File.
 *
 * Frames are numbered from 1 in the order they appear in the PixelData element.
 *
 * :param error: Pointer to error object
 * :param filehandle: File
 * :param index: One-based frame number
 *
 * :return: Frame
 */
DCM_EXTERN
DcmFrame *dcm_filehandle_read_frame(DcmError **error,
                                    DcmFilehandle *filehandle,
                                    uint32_t frame_number);
#endif