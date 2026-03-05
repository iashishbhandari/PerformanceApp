//
//  PerformanceAppTests.swift
//  PerformanceAppTests
//
//  Created by Ashish Bhandari on 05/03/26.
//

import XCTest
@testable import PerformanceApp

final class SampleAppTests: XCTestCase {

    func testExampleAddition() {
        XCTAssertEqual(2 + 2, 4, "Basic math works")
    }

    func testStringContains() {
        let str = "Hello, CI Metrics!"
        XCTAssertTrue(str.contains("CI Metrics"), "String contains expected text")
    }
}
