{
  'variables': {
    'node_engine': 'spidermonkey',

    'conditions': [
      # I'm unsure if this is SpiderNode-specific or general to Node,
      # but SpiderNode needs it (and sets it in vendor/node/common.gypi),
      # whereas Electron doesn't set it and fails without it, reporting:
      #   gyp: Undefined variable OPENSSL_PRODUCT in vendor/node/node.gyp
      ['openssl_fips != ""', {
        'OPENSSL_PRODUCT': 'libcrypto.a',
      }, {
        'OPENSSL_PRODUCT': 'libopenssl.a',
      }],
    ],
  }, # variables

  # toolchain.gypi sets CLANG_CXX_LIBRARY to libc++, which is quite reasonable
  # (and also the default on modern Macs), so I have no idea why it causes clang
  # to fail to find <tr1/type_traits>, but it does (on my Mac). Perhaps to do
  # with Electron using a custom clang instead of the system one?  In any case,
  # this fixes the problem on my Mac, although it seems wrong and feels dirty.
  # But I'm starting to get used to that feeling.
  'conditions': [
    ['clang==1', {
      'target_defaults': {
        'xcode_settings': {
          'CLANG_CXX_LIBRARY': 'libstdc++',  # -stdlib=libstdc++
        },
      },
    }],  # clang==1
  ],

  # common.gypi includes vendor/brightray/brightray.gypi, which sets -Werror
  # for all targets.  common.gypi then unsets it for a select set of targets,
  # currently ["libuv", "http_parser", "openssl", "cares", "node", "zlib"].
  #
  # But SpiderNode has many targets that generate warnings, like the targets
  # in test.gyp.  And two can play at Brightray's game.  So we disable -Werror
  # for all targets here.
  #
  # Ideally we would only disable it for the specific targets with warnings.
  # (Of course ideally Brightray wouldn't set it for all targets, or at least
  # Electron wouldn't apply Brightray's configuration to all targets.)
  #
  # TODO: disable -Werror for the specific SpiderNode targets with warnings.
  #
  'target_defaults': {
    'defines': ['NODE_ENGINE="<(node_engine)"'],
    'xcode_settings': {
      'GCC_TREAT_WARNINGS_AS_ERRORS': 'NO',
    }, # xcode_settings
  }, # target_defaults
}
